# Segrellion holding illustrations

The fortress building chains use the following holding illustrations:

- `vhalerion_holding_art.dds` — Vhalerion.
- `the_beacon_holding_art.dds` — The Beacon.
- `white_hall_holding_art.dds` — White Hall.

White Hall is loaded from exactly:

`gfx/interface/illustrations/holding_types/white_hall_holding_art.dds`

Its special-building chain references this file directly. The regular castle
levels also contain a province-specific override for province `4412`, which is
what replaces the large holding illustration.

The White Hall DDS is `2560x1168 DXT1`, which matches AGOT's standard holding
illustrations such as `northern_castle.dds` and `temple_fots.dds`. Vhalerion and
The Beacon currently use smaller custom files, but White Hall does not need to
be resized or re-exported.
