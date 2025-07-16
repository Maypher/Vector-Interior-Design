import * as migration_20250601_173010 from './20250601_173010';
import * as migration_20250605_182240 from './20250605_182240';
import * as migration_20250609_141403 from './20250609_141403';
import * as migration_20250609_221514 from './20250609_221514';
import * as migration_20250630_222416 from './20250630_222416';
import * as migration_20250701_162634 from './20250701_162634';
import * as migration_20250714_161041 from './20250714_161041';

export const migrations = [
  {
    up: migration_20250601_173010.up,
    down: migration_20250601_173010.down,
    name: '20250601_173010',
  },
  {
    up: migration_20250605_182240.up,
    down: migration_20250605_182240.down,
    name: '20250605_182240',
  },
  {
    up: migration_20250609_141403.up,
    down: migration_20250609_141403.down,
    name: '20250609_141403',
  },
  {
    up: migration_20250609_221514.up,
    down: migration_20250609_221514.down,
    name: '20250609_221514',
  },
  {
    up: migration_20250630_222416.up,
    down: migration_20250630_222416.down,
    name: '20250630_222416',
  },
  {
    up: migration_20250701_162634.up,
    down: migration_20250701_162634.down,
    name: '20250701_162634',
  },
  {
    up: migration_20250714_161041.up,
    down: migration_20250714_161041.down,
    name: '20250714_161041'
  },
];
