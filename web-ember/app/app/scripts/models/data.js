App.Data = DS.Model.extend({
	title: DS.attr('string'),
	sitename: DS.attr('string'),
	publishtime: DS.attr('string'),
	url: DS.attr('string')
});

App.Data.FIXTURES = [];
