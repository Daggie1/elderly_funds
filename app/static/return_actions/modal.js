
    var url = '';
    var hostname = $(location).attr('host');
   $(".return").click(function() {
       let id = this.id
       url = 'http://'+hostname + id
       $('#returnform').attr('action', url)
});
