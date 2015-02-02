App.BlogListView = Ember.View.extend({
   init: function(){
    this._super();
    client = $.es.Client({
           hosts: '172.20.8.3:9200',
           log: "trace"
    });
    client.search({
          index:'web-articles',
          type:'blog',
          size:50,
          body:{
            query:{
              match_all:{
              }
            },
            sort:{
             addtime:{
                order:"desc"
              }
            }
          }
        }).then(function(json){
          $.each(json.hits.hits,function(i,v){
            data = v._source
            var title = data.title
            var sitename = data.sitename
            var publishtime = (data.addtime).replace("T"," ")
            var url = data.url
            var newRow = "<tr><td><a href='"+url+"' target='_blank'>"+title+"</a></td><td>"+sitename+"</td><td>"+publishtime+"</td></tr>"
             
            $("#dataTable tbody").append(newRow);
          });
        });
  }

});