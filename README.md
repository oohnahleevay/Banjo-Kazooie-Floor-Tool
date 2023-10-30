# Banjo-Kazooie-Floor-Tool

Version 0.1

Currently capable of taking decompressed map bins as input, changing collision flags, and writing output back to original file. 
Creates a backup of the bin during import just in case you want to revert any changes.
Dummied out the texture dumping (which was always a test feature) for now until I fix the cheap workaround I'm using to load texture info. Currently causes textures to be corrupted during conversion due to mislabelling of textures in custom map models.

Future plans:
Finish writing the parser for geometry layouts and allowing import of models with bones.
Grab texture info from display lists instead of texture setup header
Label flags once I know what they all do
Allow for import of full rom file and patching floor damage functions to support custom values (knockback speed, damage type/number, sfx, etc)