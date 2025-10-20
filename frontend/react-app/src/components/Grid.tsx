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
    fetch(`api/keyframes/${video_id}`)
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
    <div className="container-lg vh-100" style={{ maxHeight: "100vh" }}>
      <div className="">
        <h1 className="text-center">{children}</h1>
        {video === undefined && (
          <h2 className="text-center">Select a video to begin</h2>
        )}
      </div>
      <div className="row" style={{ maxHeight: "50vh" }}>
        <h2>{video?.uri}</h2>
        <video
          className="object-fit-contain"
          src={"/api/videos/" + video?.rowid}
          controls
          style={{ maxHeight: "50vh" }}
        />
      </div>
      <div className="row mt-5 overflow-auto">
        <div className="d-inline-flex d-nowrap">
          {keyframes.map((keyframe, index) => (
            <div className="m-3" key={"keyframe " + index}>
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
    </div>
  );
}

export default Grid;
