cube(`CompanionActivity`, {
  sql: `SELECT * FROM companion_activity`,
  measures: {
    totalEvents: { sql: `total_events`, type: `sum` },
    avgUniqueEvents: { sql: `unique_events`, type: `avg` }
  },
  dimensions: {
    companionId: { sql: `companion_id`, type: `string`, primaryKey: true },
    windowStart: { sql: `window_start`, type: `time` }
  }
});
