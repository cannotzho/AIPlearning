import { useEffect, useState } from "react";
import Card from "./Card";

export interface Video {
  rowid: number;
  filename: string;
  uri: string;
  created: string;
}

interface Props {
  children: string;
  video?: Video;
}

function Grid({ children, video }: Props) {
  const [keyframes, setKeyframes] = useState([]);
  const getTimestamps = (video_id: number = 0) => {
    fetch(`api/videos/${video_id}`)
      .then((response) => response.json())
      .then((data) => {
        if (keyframes != data) {
          setKeyframes(data);
        }
      });
  };

  useEffect(() => {
    getTimestamps(video?.rowid);
  }, [video]);

  return (
    <>
      <h1 className="mt-2">{children}</h1>
      {video === undefined && <h2>Select a video to begin</h2>}
      <h2>{video?.uri}</h2>
      <div className="container-lg">
        <div className="row m-1">
          {keyframes.map((keyframe, index) => (
            <div className="col-sm-12 col-xl-4 m-5" key={"keyframe " + index}>
              <Card
                image_url={video?.uri}
                frame_number={index}
                date_created={video?.created}
                frame_timestamp={keyframe}
              />
            </div>
          ))}
        </div>
      </div>
    </>
  );
}

export default Grid;
