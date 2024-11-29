# Banjo-Kazooie-Floor-Tool

Version 0.2

Currently capable of taking decompressed map bins as input, changing collision flags, and writing output back to original file. 
Creates a backup of the bin during import just in case you want to revert any changes.
Custom map models now import properly, and there shouldn't be any Geo Layout Commands that it can't handle.

Future plans:
Grab texture info from display lists instead of texture setup header
Label flags once I know what they all do
Allow for import of full rom file and patching floor damage functions to support custom values (knockback speed, damage type/number, sfx, etc)
