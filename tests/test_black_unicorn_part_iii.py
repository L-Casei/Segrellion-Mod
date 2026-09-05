"""Regression checks interpreting the actual Part III scheduling scripts.

This small interpreter covers flags, scopes, triggers and delayed events only;
it does not replace an in-game test of CK3's event UI or the ensuing story.
Run: python -m unittest discover -s tests -v
"""
from pathlib import Path
import heapq
import re
import unittest

ROOT = Path(__file__).resolve().parents[1]
PREFIX = 'segrellion_black_unicorn_'
DAEMON = 'character:Segrellion_60'
VISENYA = 'character:Black_Unicorn_1'


def body(source, key, indent=r'[ \t]*'):
    match = re.search(r'(?m)^' + indent + re.escape(key) + r'\s*=\s*\{', source)
    assert match, key
    start = match.end()
    depth = 1
    for token in re.finditer(r'#[^\n]*|"[^"\n]*"|[{}]', source[start:]):
        if token[0] == '{':
            depth += 1
        elif token[0] == '}':
            depth -= 1
            if depth == 0:
                return source[start:start + token.start()]
    raise AssertionError('Unclosed block: ' + key)


def parse(source):
    source = re.sub(r'#[^\n]*', '', source)
    tokens = re.findall(r'\?=|=|[{}]|[^\s{}=]+', source)
    pos = 0

    def entries():
        nonlocal pos
        result = []
        while pos < len(tokens) and tokens[pos] != '}':
            key, op = tokens[pos:pos + 2]
            assert op in ('=', '?='), (key, op)
            pos += 2
            value = tokens[pos]
            pos += 1
            if value == '{':
                value = entries()
                assert tokens[pos] == '}'
                pos += 1
            result.append((key, op, value))
        return result

    result = entries()
    assert pos == len(tokens)
    return result


def fields(node):
    return {key: value for key, _, value in node}


EFFECT_SOURCE = (ROOT / 'common/scripted_effects/segrellion_black_unicorn_effects.txt').read_text(encoding='utf-8-sig')
EVENT_SOURCE = (ROOT / 'events/segrellion_black_unicorn_events.txt').read_text(encoding='utf-8-sig')
TRIGGERS = fields(parse((ROOT / 'common/scripted_triggers/segrellion_black_unicorn_part_iii_triggers.txt').read_text()))
START = PREFIX + 'start_post_beacon_clock_effect'
PROGRESS = PREFIX + 'post_beacon_progression_effect'
TRY = PREFIX + 'try_start_post_beacon_part_iii_effect'
EFFECTS = {key: parse(body(EFFECT_SOURCE, key)) for key in (START, PROGRESS, TRY)}
EVENTS = {number: parse(body(body(EVENT_SOURCE, 'segrellion_black_unicorn.' + number), 'immediate')) for number in ('0598', '0599')}
ENTRY_TRIGGER = parse(body(body(EVENT_SOURCE, 'segrellion_black_unicorn.0600'), 'trigger', indent='\t'))


class Simulation:
    def __init__(self):
        self.day = 0
        self.flags = {DAEMON: {}, VISENYA: {}}
        self.alive = {DAEMON: True, VISENYA: True}
        self.prison = {DAEMON: False, VISENYA: False}
        self.titles = {'title:c_farring_cross'}
        self.queue = []
        self.delivered = []
        self.flag('route_d_resolved')

    def flag(self, suffix, days=None, actor=DAEMON):
        self.flags[actor][PREFIX + suffix] = None if days is None else self.day + days

    def has(self, name, actor):
        return name in self.flags[actor] and (self.flags[actor][name] is None or self.flags[actor][name] > self.day)

    def condition(self, node, actor=DAEMON):
        def check(key, value):
            if key in ('AND', 'OR', 'NOT'):
                results = [check(k, v) for k, _, v in value]
                return any(results) if key == 'OR' else not any(results) if key == 'NOT' else all(results)
            if key in TRIGGERS:
                return self.condition(TRIGGERS[key], actor)
            if key.startswith('character:'):
                return key in self.alive and self.condition(value, key)
            if key == 'this':
                return actor == value
            if key == 'exists':
                return value in self.alive
            if key == 'is_alive':
                return self.alive[actor] == (value == 'yes')
            if key == 'is_imprisoned':
                return self.prison[actor] == (value == 'yes')
            if key == 'has_character_flag':
                return self.has(value, actor)
            if key == 'has_title':
                return actor == DAEMON and value in self.titles
            raise AssertionError(('Unhandled trigger', key))
        return all(check(key, value) for key, _, value in node)

    def run(self, node, actor=DAEMON):
        for key, _, value in node:
            if key == 'if':
                if self.condition(fields(value)['limit'], actor):
                    self.run([entry for entry in value if entry[0] != 'limit'], actor)
            elif key.startswith('character:'):
                if key in self.alive:
                    self.run(value, key)
            elif key == 'add_character_flag':
                data = fields(value) if isinstance(value, list) else {'flag': value}
                self.flags[actor][data['flag']] = self.day + int(data['days']) if 'days' in data else None
            elif key == 'remove_character_flag':
                self.flags[actor].pop(value, None)
            elif key == 'trigger_event':
                data = fields(value)
                heapq.heappush(self.queue, (self.day + int(data['days']), data['id'].split('.')[-1]))
            elif key in EFFECTS:
                self.run(EFFECTS[key], actor)
            elif key not in ('give_nickname', PREFIX + 'resolve_secret_effect'):
                raise AssertionError(('Unhandled effect', key))

    def advance(self, day):
        while self.queue and self.queue[0][0] <= day:
            self.day, event = heapq.heappop(self.queue)
            if event == '0600':
                if self.condition(ENTRY_TRIGGER):
                    self.delivered.append(self.day)
                    # Milestones set by 0600's immediate; later story is outside this test.
                    self.flag('post_beacon_started')
                    self.flag('daemon_abducted_in_beacon')
                self.flags[DAEMON].pop(PREFIX + 'post_beacon_queued', None)
            else:
                self.run(EVENTS[event])
        self.day = day


class PartIIIRegressionTests(unittest.TestCase):
    def test_beacon_without_empire_or_war_flag_starts_after_one_year(self):
        sim = Simulation()
        sim.run(EFFECTS[START])
        sim.advance(365)
        self.assertEqual(sim.delivered, [])
        sim.advance(800)
        self.assertEqual(sim.delivered, [366])

    def test_v2_save_with_missing_route_pair_recovers_after_eight_days(self):
        sim = Simulation()
        sim.flag('post_beacon_clock_v2')
        sim.flag('post_beacon_clock_started')
        sim.flag('post_beacon_queued')
        sim.run(EFFECTS[PROGRESS])
        sim.advance(100)
        self.assertEqual(sim.delivered, [8])

    def test_legacy_running_timer_is_preserved_even_if_event_was_lost(self):
        sim = Simulation()
        sim.flag('post_beacon_waiting_year', days=100)
        sim.run(EFFECTS[PROGRESS])
        sim.advance(99)
        self.assertEqual(sim.delivered, [])
        sim.advance(150)
        self.assertEqual(sim.delivered, [121])

    def test_imprisonment_retries_and_rechecks_event_delivery(self):
        for actor in (DAEMON, VISENYA):
            with self.subTest(actor=actor):
                sim = Simulation()
                sim.run(EFFECTS[START])
                sim.advance(365)
                sim.prison[actor] = True  # Between queueing and delivery.
                sim.advance(400)
                self.assertEqual(sim.delivered, [])
                sim.prison[actor] = False
                sim.advance(500)
                self.assertEqual(sim.delivered, [421])

    def test_stale_watchdog_cannot_skip_year(self):
        sim = Simulation()
        sim.run(EFFECTS[START])
        sim.day = 7
        sim.run(EVENTS['0599'])
        sim.advance(800)
        self.assertEqual(sim.delivered, [366])

    def test_real_quarterly_hook_can_rebuild_lost_controller(self):
        sim = Simulation()
        sim.run(EFFECTS[START])
        sim.queue.clear()
        sim.day = 400
        sim.run(EFFECTS[PROGRESS])
        sim.advance(500)
        self.assertEqual(sim.delivered, [401])
        actions = (ROOT / 'common/on_action/segrellion_on_actions.txt').read_text()
        self.assertIn('segrellion_black_unicorn_post_beacon_quarterly_recovery', body(actions, 'quarterly_playable_pulse'))

    def test_both_supported_routes_and_empire_alternative(self):
        for route in ('route_d_resolved', 'route_c_destiny', 'destiny_route_pending'):
            sim = Simulation()
            sim.flags[DAEMON].clear()
            sim.flag(route)
            sim.titles = {'title:e_flamelands'}
            sim.run(EFFECTS[START])
            sim.advance(400)
            self.assertEqual(sim.delivered, [366])

    def test_wrong_route_dead_joined_or_completed_stories_do_not_start(self):
        for case in ('wrong_route', 'no_land', 'dead', 'missing', 'joined', 'resolved', 'abducted'):
            with self.subTest(case=case):
                sim = Simulation()
                if case == 'wrong_route': sim.flags[DAEMON].clear()
                if case == 'no_land': sim.titles.clear()
                if case == 'dead': sim.alive[VISENYA] = False
                if case == 'missing': del sim.alive[VISENYA]
                if case == 'joined': sim.flag('visenya_joined_daemon', actor=VISENYA)
                if case == 'resolved': sim.flag('post_beacon_resolved')
                if case == 'abducted': sim.flag('daemon_abducted_in_beacon')
                sim.run(EFFECTS[START])
                sim.run(EFFECTS[PROGRESS])
                sim.advance(800)
                self.assertEqual(sim.delivered, [])

    def test_stale_started_flag_recovers_but_delivered_story_never_repeats(self):
        sim = Simulation()
        sim.flag('post_beacon_started')
        sim.run(EFFECTS[PROGRESS])
        sim.advance(100)
        sim.run(EFFECTS[PROGRESS])
        sim.advance(900)
        self.assertEqual(sim.delivered, [8])


if __name__ == '__main__':
    unittest.main()
