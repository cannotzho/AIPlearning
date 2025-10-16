import { ReactNode, useEffect, useState } from "react";
import Alert from "./components/Alert";
import Button from "./components/Button";
import Grid from "./components/Grid";
import Card from "./components/Card";
import ListGroup from "./components/ListGroup";
import Searchbar from "./components/Searchbar";
import UploadBtn from "./components/UploadBtn";

interface Video {
  rowid: number;
  filename: string;
  uri: string;
  created: string;
}

function App() {
  const [displayedVideos, setDisplayedVideos] = useState<Video[]>([]);
  const [selectedVideo, setSelectedVideoIndex] = useState<Video>();

  const getVideos = () => {
    fetch("/api/videos/")
      .then((response) => response.json())
      .then((data) => setDisplayedVideos(data));
  };

  useEffect(() => {
    getVideos();
  }, [displayedVideos]);

  const displayVideoDetails = (video: Video) => {
    // Get details of video via video name and set state of video_keyframes with new information
    setSelectedVideoIndex(video);
  };

  return (
    <div className="container-lg">
      <div className="row">
        <div className="col-4 bg-secondary rounded-4 mt-2" key="sidebar">
          {/* Column for sidebar */}

          {/* Upload Button */}
          <UploadBtn upload_route="/api/process" />
          {/* Searchbar */}
          <Searchbar option1="Detected Objects" option2="Filename" />
          {/* Video List, might refactor this to type-safety for items next time... */}
          <ListGroup
            videos={displayedVideos}
            heading="Processed Videos"
            onSelectItem={displayVideoDetails}
          />
        </div>
        <div className="col-8 mt-2 bg-info rounded-4" key="main">
          {/* Column for main content */}
          <Grid video={selectedVideo}>Video Details</Grid>
        </div>
      </div>
    </div>
  );
}

export default App;
