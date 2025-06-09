import * as migration_20250601_173010 from './20250601_173010';
import * as migration_20250605_182240 from './20250605_182240';
import * as migration_20250609_141403 from './20250609_141403';

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
    name: '20250609_141403'
  },
];
