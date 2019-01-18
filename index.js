window.onload = () => {
  console.log('hello from js');
};

window.onwebchannel = function () {
  window.mediaPlayerBridge.positionChanged.connect(function (position) {
    document.getElementById('position').innerText = Math.round(position / 1000); // in milliseconds
  });

  document.getElementById('playStopButton').onclick = () => {
    window.mediaPlayerBridge.playStop();
  };
}