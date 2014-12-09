App.ListView = Ember.View.extend({
	tagName : 'li',
	classNameBindings : ['active'],

	active: function(){
		return this.get('chlidViews.firstObject.active');
	}.property()
});
