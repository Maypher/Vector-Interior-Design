import * as migration_20250601_173010 from './20250601_173010';

export const migrations = [
  {
    up: migration_20250601_173010.up,
    down: migration_20250601_173010.down,
    name: '20250601_173010'
  },
];
