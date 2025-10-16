interface Props {
  option1: string;
  option2: string;
}

const Searchbar = ({ option1 = "option1", option2 = "option2" }: Props) => {
  return (
    <form className="row gy-2 gx-3 align-items-center">
      <div className="col-auto">
        <label className="visually-hidden" htmlFor="search_query">
          Search
        </label>
        <input
          type="text"
          className="form-control"
          id="search_query"
          placeholder="Search..."
        />
      </div>
      <div className="col-auto">
        <div className="form-check">
          <input
            className="form-check-input"
            type="radio"
            name="gridRadios"
            id="objects_search"
            value="objects_search"
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
            name="gridRadios"
            id="filenames_search"
            value="filenames_search"
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
