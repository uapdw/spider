App.List = DS.Model.extend({
	title: DS.attr('string'),
	routing: DS.attr('string')
});

App.List.FIXTURES = [{
	id: 1,
	title: '新闻列表',
	routing: 'news'
}, {
	id: 2,
	title: '百度新闻列表',
	routing: 'baidu'
}, {
	id: 3,
	title: '报告列表',
	routing: 'report'
},{
	id: 4,
	title: '博客列表',
	routing: 'blog'
}];

App.News = Ember.Object.create({
	title: '新闻列表'
});
App.Baidu = Ember.Object.create({
	title: '百度新闻列表'
});
App.Report = Ember.Object.create({
	title: '报告列表'
});
App.Blog = Ember.Object.create({
	title: '博客列表'
});

