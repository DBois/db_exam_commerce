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
	role: 'logisticAdmin',
	privileges: [
		{
			actions: ['find', 'insert', 'update', 'remove'],
			resource: { db: 'db_exam_orders', collection: 'orders' },
		},
	],
	roles: [],
});

db.createUser({
	user: 'dboisSupport',
	pwd: 'dbois',
	roles: ['customerSupport'],
});

db.createUser({
	user: 'dboisAdmin',
	pwd: 'dbois',
	roles: ['customerSupport'],
});
