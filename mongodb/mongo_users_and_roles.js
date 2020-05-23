db.createRole({
	role: 'customerSupport',
	privileges: [
		{
			actions: ['find', 'update'],
			resource: { db: 'db_exam_orders', collection: 'orders' },
		},
	],
	roles: [],
});

db.createRole({
	privileges: [],
	role: 'logisticAdmin',
	roles: [{ role: 'readWrite', db: 'db_exam_orders' }],
});

db.createUser({
	user: 'dboisSupport',
	pwd: 'dbois',
	roles: ['customerSupport'],
});

db.createUser({
	user: 'dboisAdmin',
	pwd: 'dbois',
	roles: ['logisticAdmin'],
});
