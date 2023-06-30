import React, { useEffect, useRef, useState } from 'react';
import ReactPlayer from 'react-player';

const VideoClip = ({ videoUrl, start, end }) => {
  const playerRef = useRef(null);
  const [playing, setPlaying] = useState(true);
  const [progress, setProgress] = useState(0);
  const [duration, setDuration] = useState(0);
  const [marking, setMarking] = useState(false);
  const [marks, setMarks] = useState([]);

  useEffect(() => {
    if (playerRef.current && start < duration) {
      playerRef.current.seekTo(start, 'seconds');
    }
  }, [start, duration]);

  const handleProgress = ({ playedSeconds }) => {
    if (playedSeconds >= end) {
      setPlaying(false);
    } else {
      setProgress(playedSeconds - start);
    }
  };

  const handleStartMark = () => {
    const currentTime = playerRef.current.getCurrentTime();
    setMarks((prevMarks) => [...prevMarks, { start: currentTime, end: null }]);
    setMarking(true);
  };

  const handleEndMark = () => {
    const currentTime = playerRef.current.getCurrentTime();
    setMarks((prevMarks) => {
      const newMarks = prevMarks.map((mark) =>
        mark.end === null ? { ...mark, end: currentTime } : mark
      );
      return newMarks;
    });
    setMarking(false);
  };

  const handleSeek = (e) => {
    const newTime = parseFloat(e.target.value) + start;
    setProgress(newTime - start);
    playerRef.current.seekTo(newTime, 'seconds');
  };

  const handlePlay = () => {
    const currentTime = playerRef.current.getCurrentTime();
    if (currentTime < start || currentTime > end) {
      playerRef.current.seekTo(start, 'seconds');
    }
    setPlaying(true);
  };

  const handleDuration = (duration) => {
    setDuration(duration);
  };

  const handleError = (e) => {
    console.error('Error al cargar o reproducir el video:', e);
  };

  const secondsToMinutes = (seconds) => {
    const min = Math.floor(seconds / 60);
    const sec = Math.floor(seconds % 60);
    return `${min}:${sec < 10 ? '0' : ''}${sec}`;
  };

  return (
    <div>
      <h2>Evento</h2>
      <ReactPlayer
        ref={playerRef}
        url={videoUrl}
        playing={playing}
        onProgress={handleProgress}
        onPlay={handlePlay}
        onDuration={handleDuration}
        onError={handleError}
        controls
      />
      <button onClick={handleStartMark} disabled={marking}>Marcar inicio del intervalo</button>
      <button onClick={handleEndMark} disabled={!marking}>Marcar final del intervalo</button>
      <div style={{ display: 'flex', alignItems: 'center' }}>
        <input
          type="range"
          min={0}
          max={end - start}
          value={progress}
          onChange={handleSeek}
          style={{ width: '100%', height: '50px' }}
        />
        <div>{secondsToMinutes(progress)}</div>
      </div>
      <button onClick={() => setPlaying(!playing)}>
        {playing ? 'Pause' : 'Play'}
      </button>
      <table>
        <thead>
          <tr>
            <th>Inicio</th>
            <th>Final</th>
          </tr>
        </thead>
        <tbody>
          {marks.map((mark, index) => (
            <tr key={index}>
              <td>{secondsToMinutes(mark.start)}</td>
              <td>{mark.end ? secondsToMinutes(mark.end) : '-'}</td>
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
};

export default VideoClip;