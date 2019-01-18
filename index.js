window.onload = () => {
  console.log('hello from js');
};

window.onwebchannel = function () {
  console.log('onwebchannel()');
  // console.log(window.jshelper);
  console.log(window.mediaPlayerBridge);

  window.mediaPlayerBridge.positionChanged.connect(function (position) {
    console.log('positionChanged', position);
    document.getElementById('position').innerText = Math.round(position / 1000); // in milliseconds
  });

  document.getElementById('playStopButton').onclick = () => {
    window.mediaPlayerBridge.playStop();
  };
}