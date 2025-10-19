import { ReactNode, useEffect, useState } from "react";
import Alert from "./components/Alert";
import Button from "./components/Button";
import Grid, { Video } from "./components/Grid";
import Card from "./components/Card";
import ListGroup from "./components/ListGroup";
import Searchbar from "./components/Searchbar";
import UploadBtn from "./components/UploadBtn";

function App() {
  const [displayedVideos, setDisplayedVideos] = useState<Video[]>([]);
  const [selectedVideo, setSelectedVideo] = useState<Video>();

  const getVideos = () => {
    fetch("/api/videos/")
      .then((response) => response.json())
      .then((data) => setDisplayedVideos(data));
  };

  useEffect(() => {
    getVideos();
  }, []);

  const handleSearch = (videos: Video[]) => {
    setDisplayedVideos(videos);
    if (videos) {
      setSelectedVideo(videos[0]);
    } else {
      console.log("set video failed");
    }
  };

  return (
    <div className="container-xxl">
      <div className="row">
        <div className="col-4 bg-secondary rounded-4 mt-2" key="sidebar">
          {/* Column for sidebar */}

          {/* Upload Button */}
          <UploadBtn upload_route="/api/process" />
          {/* Searchbar */}
          <Searchbar
            option1="Detected Objects"
            option2="Filename"
            handleResponse={handleSearch}
          />
          {/* Video List, might refactor this to type-safety for items next time... */}
          <ListGroup
            videos={displayedVideos}
            heading="Processed Videos"
            onSelectItem={setSelectedVideo}
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
