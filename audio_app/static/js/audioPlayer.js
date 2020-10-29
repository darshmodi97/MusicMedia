function audioPlayer(){

    var currentSong = 0;
    $("#audioPlayer")[0].src = $("#playlist td a")[currentSong];
    $("#audioPlayer")[0].play();
    $($("#playlist td a")[currentSong]).parent().addClass('current-song')


    $("#previous").click(function(e){
        e.preventDefault();
//        console.log("before --",currentSong)
        currentSong --;
//        console.log("after --",currentSong)
        if(currentSong == -1 ){
//            console.log("in if")
            currentSong = ($("#playlist td a").length) -1;
        }
        $("#playlist td").removeClass("current-song");
        $($("#playlist td a")[currentSong]).parent().addClass("current-song");
        $("#audioPlayer")[0].src = $("#playlist td a")[currentSong];
        $("#audioPlayer")[0].play();

    });


    $("#next").click(function(e){
        e.preventDefault();
        currentSong ++;
        if(currentSong >= $("#playlist td a").length){
            currentSong = 0;
        }
        $("#playlist td").removeClass("current-song");
        $($("#playlist td a")[currentSong]).parent().addClass("current-song");
        $("#audioPlayer")[0].src = $("#playlist td a")[currentSong];
        $("#audioPlayer")[0].play();

    });


    $("#playlist td a").click(function(e){
       e.preventDefault();
       $("#audioPlayer")[0].src = this;
       $("#audioPlayer")[0].play();
       $("#playlist td").removeClass("current-song");
        //console.log("before:",currentSong)

        currentSong = $(this).attr("data-link_id")
        //console.log("after:",currentSong)
        $(this).parent().addClass("current-song");

    });

    $("#audioPlayer")[0].addEventListener("ended", function(){
       //console.log("song ended")
       //console.log("before added:",currentSong)
       currentSong++;
       //console.log("after added :",currentSong)
        if(currentSong >= $("#playlist td a").length){
            currentSong = 0;
        }
        //console.log("after if case:",currentSong)
        $("#playlist td").removeClass("current-song");
        $($("#playlist td a")[currentSong]).parent().addClass("current-song");
        $("#audioPlayer")[0].src = $("#playlist td a")[currentSong];
        $("#audioPlayer")[0].play();
    });
}