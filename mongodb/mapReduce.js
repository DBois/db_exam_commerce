db.orders.mapReduce(
	function () {
		const products = this.Products;

		products.forEach((product) => {
			emit(product.ProductNo, product.Quantity);
		});
	},
	function (key, values) {
		// Could just use values.length to get count
		return Array.sum(values);
	},
	{
		query: {
			Products: { $exists: true },
			InvoiceDate: { $gte: new Date(ISODate().getTime() - 1000 * 3600 * 24 * 30) },
		},
		out: 'mostPopularProducts',
	}
);
