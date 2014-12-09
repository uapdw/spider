App.ApplicationRoute = Ember.Route.extend({
    // admittedly, this should be in IndexRoute and not in the
    // top level ApplicationRoute; we're in transition... :-)
	beforeModel: function(){
		this.transitionTo('news');
	},
    model: function() {
    	
	}
});
