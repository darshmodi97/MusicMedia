function my_audio_player(myParam){

    console.log("id :",myParam)

    var a = $("#playlist td a[data-song_id="+myParam+"]") // getting an element(<a>) by its property named: data-song_id
    console.log(a[0])
    $(a).parent().addClass('current-song')
    var playback_number = $(a).attr('data-link_id') // getting another property value of that element..
    console.log(playback_number)
    currentSong = playback_number

    $("#audioPlayer")[0].addEventListener("ended", function(){
//       console.log("before add ",currentSong)
       currentSong ++;
//       console.log("after add ",currentSong)
        if(currentSong >= $("#playlist td a").length){
            currentSong = 0;
        }

        $("#playlist td").removeClass("current-song");
        $($("#playlist td a")[currentSong]).parent().addClass("current-song");
        var url= window.location.origin; // will give domain name for now it will be : "http://127.0.0.1:8000"
        var get_new_id = $("#playlist td a[data-link_id="+currentSong+"]")
        var next_id = $(get_new_id).attr('data-song_id')
        location.replace(url+"/play_song?id="+next_id)
    });

}