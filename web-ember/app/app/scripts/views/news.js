App.NewsListView = Ember.View.extend({
   init: function(){
    this._super();
    client = $.es.Client({
           hosts: '172.20.8.3:9200',
           log: "trace"
    });
    client.search({
          index:'web-articles',
          type:'article',
          size:50,
          body:{
            query:{
              match_all:{
              }
            },
            sort:{
              publishtime:{
                order:"desc"
              }
            }
          }
        }).then(function(json){
          $.each(json.hits.hits,function(i,v){
            data = v._source;
            var title = data.title;
            var sitename = data.sitename;
            //var content = subString(data.content,100,true)
            var content = subString((data.content).replace(/<\/?[^>]*>/g,''),200,true);
            var publishtime = (data.publishtime).replace("T"," ");
            var url = data.url;
            var newRow = "<tr><td><a href='"+url+"' target='_blank'>"+title+"</a></td><td>"+sitename+"</td><td>"+publishtime+"</td></tr>";
            var strNewRow = "<tr><td><div class='media'><div class='media-body'> <h4 class='media-heading'><a href='" + url + "'>" + title + "</a></h4><p>" + content + "</p><p class='txt-green'>" + publishtime + " - " + sitename  + "</p></div> </div></td></tr>";
              
            $("#dataTable1 tbody").append(strNewRow);
          });
  });
  }
});