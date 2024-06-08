import { useState, useRef, useEffect } from 'react';

interface AudioPlayerProps {
  audioUrl: string;
}

const AudioPlayer: React.FC<AudioPlayerProps> = ({ audioUrl }) => {
  const [isPlaying, setIsPlaying] = useState(false);
  const [currentTime, setCurrentTime] = useState(0);
  const audioRef = useRef<HTMLAudioElement| null>(null);

  useEffect(() => {
    return () => {
      // Clean up the ref when the component unmounts
      audioRef.current = null;
    };
  }, []);

  const togglePlay = () => {
    if (isPlaying) {
      audioRef.current?.pause();
    } else {
      audioRef.current?.play();
    }
    setIsPlaying(!isPlaying);
  };

  const handleTimeUpdate = (e: React.SyntheticEvent<HTMLAudioElement>) => {
    setCurrentTime(e.currentTarget.currentTime);
  };

  return (
    <div className="audio-player">
      <div className='text-2xl font-bold'>
        Audio Recording of Animal
      </div>
      <audio
        controls
        ref={audioRef}
        src={audioUrl}
        onTimeUpdate={handleTimeUpdate}
        onEnded={() => setIsPlaying(false)}
      ></audio>

      {/* <div>
        {audioUrl}
      </div> */}
      <div className="controls">
        {/* <button onClick={togglePlay}>
          {isPlaying ? 'Pause' : 'Play'}
        </button> */}
        <div className="time font-bold">{currentTime.toFixed(1)} seconds</div>
      </div>
    </div>
  );
};

export default AudioPlayer;
