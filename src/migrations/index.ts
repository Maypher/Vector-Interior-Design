import * as migration_20250601_173010 from './20250601_173010';
import * as migration_20250605_182240 from './20250605_182240';

export const migrations = [
  {
    up: migration_20250601_173010.up,
    down: migration_20250601_173010.down,
    name: '20250601_173010',
  },
  {
    up: migration_20250605_182240.up,
    down: migration_20250605_182240.down,
    name: '20250605_182240'
  },
];
