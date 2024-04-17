document.addEventListener('DOMContentLoaded', function() {
    const audioContainers = document.querySelectorAll(".audio-container");

    audioContainers.forEach(function(container) {
        const audio = container.querySelector(".audio");
        const playBtn = container.querySelector(".play-btn");
        const stopBtn = container.querySelector(".stop-btn");
        const muteBtn = container.querySelector(".mute-btn");
        const volumeSlider = container.querySelector(".volume-slider");
        const trackFile = audio.querySelector("source").getAttribute("src");

        const audioTrack = WaveSurfer.create({
            container: audio,
            waveColor: "#eee",
            progressColor: "red",
            barWidth: 2,
        });

        audioTrack.load(trackFile);

        playBtn.addEventListener("click", () => {
            audioTrack.playPause();

            if (audioTrack.isPlaying()) {
                playBtn.classList.add("playing");
            } else {
                playBtn.classList.remove("playing");
            }
        });

        stopBtn.addEventListener("click", () => {
            audioTrack.stop();
            playBtn.classList.remove("playing");
        });

        volumeSlider.addEventListener("mouseup", () => {
            changeVolume(volumeSlider.value);
        });

        const changeVolume = (volume) => {
            if (volume == 0) {
                muteBtn.classList.add("muted");
            } else {
                muteBtn.classList.remove("muted");
            }

            audioTrack.setVolume(volume);
        };

        muteBtn.addEventListener("click", () => {
            if (muteBtn.classList.contains("muted")) {
                muteBtn.classList.remove("muted");
                audioTrack.setVolume(0.5);
                volumeSlider.value = 0.5;
            } else {
                audioTrack.setVolume(0);
                muteBtn.classList.add("muted");
                volumeSlider.value = 0;
            }
        });
    });
});
