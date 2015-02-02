App.Router.map(function () {
  // Add your routes here
  
  this.resource('list', {path: '/'}, function(){
 	this.resource('news', {path: 'news'});
    this.resource('baidu', {path: 'baidu'});
    this.resource('report', {path: 'report'}); 
    this.resource('blog', {path: 'blog'});	
  });

//	this.resource('list', {path: '/:routing'});

});
