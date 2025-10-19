import { FormEvent, FormEventHandler, useState } from "react";
import { Video } from "./Grid";

interface Props {
  option1: string;
  option2: string;
  handleResponse?: (videos: Video[]) => void;
}

const Searchbar = ({
  option1 = "option1",
  option2 = "option2",
  handleResponse = (videos) => {
    videos.map((video) => {
      console.log(video.uri);
    });
  },
}: Props) => {
  const [query, setQuery] = useState("");
  const [search_type, setSearchType] = useState(1);

  const handleSubmit = async (event: FormEvent) => {
    event.preventDefault();

    await fetch(`/api/search/?query=${query}&search_type=${search_type}`, {
      headers: {
        "Content-Type": "application/json",
      },
    })
      .then((response) => response.json())
      .then((data) => handleResponse(data));
  };
  return (
    <form className="row gy-2 gx-3 align-items-center" onSubmit={handleSubmit}>
      <div className="col-auto">
        <label className="visually-hidden" htmlFor="search_query">
          Search
        </label>
        <input
          type="text"
          className="form-control"
          name="query"
          value={query}
          id="search_query"
          placeholder="Search..."
          onChange={(e) => setQuery(e.target.value)}
        />
      </div>
      <div className="col-auto">
        <div className="form-check">
          <input
            className="form-check-input"
            type="radio"
            name="search_type"
            id={option1 + "_search"}
            onChange={(e) => setSearchType(1)}
            defaultChecked
          />
          <label className="form-check-label" htmlFor={option1 + "_search"}>
            {option1}
          </label>
        </div>
        <div className="form-check">
          <input
            className="form-check-input"
            type="radio"
            name="search_type"
            id={option2 + "_search"}
            onChange={(e) => setSearchType(0)}
          />
          <label className="form-check-label" htmlFor={option2 + "_search"}>
            {option2}
          </label>
        </div>
      </div>
      <div className="col-auto">
        <button type="submit" className="btn btn-primary">
          Submit
        </button>
      </div>
    </form>
  );
};

export default Searchbar;
