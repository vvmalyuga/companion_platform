cube(`CompanionActivity`, {
  sql: `SELECT * FROM companion.gold_business_metrics`,

  measures: {
    UserCount: { sql: `user_count`, type: `sum` },
    BookingCount: { sql: `booking_count`, type: `sum` },
    AvgRating: { sql: `avg_rating`, type: `avg` },
    Revenue: { sql: `revenue`, type: `sum`, format: `currency` },
    ActiveCompanions: { sql: `active_companions`, type: `sum` }
  },

  dimensions: {
    category: { sql: `category`, type: `string` },
    city: { sql: `city`, type: `string` },
    age_group: { sql: `multiIf(user_count < 10, 'new', user_count < 100, 'growth', 'scale')`, type: `string` },
    subscription_type: { sql: `subscription_type`, type: `string` },
    booking_status: { sql: `booking_status`, type: `string` },
    metricDate: { sql: `metric_date`, type: `time` }
  }
});
