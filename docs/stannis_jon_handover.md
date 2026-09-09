# Stannis / Jon fix

Base: main 1bea3ee, retaining 961d55a. AGOT 0.5.2.1 verified at
C:/Program Files (x86)/Steam/steamapps/workshop/content/1158310/2962333032.
The neighbouring GOT ORIGINAL MOD copy is older (0.4.40).

Native source files relative to that installation:

- common/scripted_triggers/00_agot_triggers.txt: agot_is_independent_ruler
  excludes agot_pwl_direct and bookmark_independent; the Westerosi lord
  predicate combines that political status with realm geography.
- common/customizable_localization/00_agot_holder_feudal_custom_loc.txt:
  FEUDAL_EMPIRE_MALE uses lord_non_paramount for historic ruling houses,
  lord_paramount otherwise. North/Stark and Vale/Arryn have historic_lord_house
  in history/titles/agot_e_the_north.txt and agot_e_the_vale.txt. Reach,
  Stormlands and Riverlands use the general paramount branch unless exceptional
  contracts apply. Jon can therefore use the native historic-Stark form Lord Jon.
- common/flavorization/00_agot_title_holders.txt links ruler rank to this
  dynamic localization. No custom flavorization or duplicated Lord text needed.
- common/scripted_effects/00_agot_mega_wars_effects.txt documents the political
  liege variables; agot_reassign_pwl_direct_effect restores actual vassalage
  only with a higher-ranking liege. Without a hegemony Stannis cannot be the
  mechanical liege of empire-tier Jon: the relation is political, as in AGOT.
- common/scripted_triggers/00_agot_government_triggers.txt makes lp_feudal
  depend on membership in a paramountcy realm, not on royal/lord wording.
  An independent North normally uses feudal. The verified native effect
  agot_on_change_government_data_effect refreshes government naming data.
  assign_character_parameter_effect computes temporary naming scopes;
  apply_character_special_title_data handles dowagers, not title refresh.
- common/scripted_triggers/00_agot_coronation_triggers.txt and
  10_ach_scripted_triggers.txt: both coronation systems require
  agot_ruler_requires_coronation and thus AGOT independence. The old
  agot_start_historical_coronation_cooldown flag is unused in this version.
  A small predicate override excludes only pre-Council Jon, also in old saves.

The old handover returned e_the_north to Stannis and forced k_winterfell
primary; government alone did not establish the native political lord state.
Jon now retains the North, Winterfell and northern vassals. Existing saves
are repaired by the monthly progression. Council acclamation clears the lock.
The letter records pending news on Jon before death; old saves recover using
has_dead_character_flag. Receipt prevents duplicate windows. Delays are 3+3
and one day for the death notice. Missing response and opinion loc are added.
Ramsay must participate on the defeated combat side, not just share a province.

In-game verification remains necessary: player switch, Watch succession,
real title/vassal transfer, political liege through AGOT megawar maintenance,
native Lord wording, coronations blocked before/during the interregnum,
one death letter, Council King wording and released eligibility. Test AI and
player, new/old saves, and Ramsay present/absent/already imprisoned/dead.
