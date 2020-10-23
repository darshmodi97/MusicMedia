  function audioPlayer(){
            var currentSong = 0;
            $("#audioPlayer")[0].src = $("#playlist td a")[0];
            $("#audioPlayer")[0].play();
            $("#playlist td a").click(function(e){
               e.preventDefault();
               $("#audioPlayer")[0].src = this;
               $("#audioPlayer")[0].play();
               $("#playlist td").removeClass("current-song");
                currentSong = $(this).parent().index();
                $(this).parent().addClass("current-song");
            });

            $("#audioPlayer")[0].addEventListener("ended", function(){
               currentSong++;
                if(currentSong == $("#playlist td a").length)
                    currentSong = 0;
                $("#playlist td").removeClass("current-song");
                $("#playlist td:eq("+currentSong+")").addClass("current-song");
                $("#audioPlayer")[0].src = $("#playlist td a")[currentSong].href;
                $("#audioPlayer")[0].play();
            });
        }