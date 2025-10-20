import React, { ChangeEvent, FormEvent, useState } from "react";

interface Props {
  upload_route: string;
}

const UploadBtn = ({ upload_route }: Props) => {
  const [buttonDisabled, setButtonDisabled] = useState(true);

  const handleUpload = (e: ChangeEvent<HTMLInputElement>) => {
    if (e.target.files && e.target.files[0]) {
      setButtonDisabled(false);
    } else {
      setButtonDisabled(true);
    }
  };

  return (
    <>
      <form action={upload_route} method="POST" encType="multipart/form-data">
        <div className="input-group mb-3">
          <input
            type="file"
            className="form-control"
            id="videoInput"
            name="video"
            onChange={handleUpload}
          />
          <label className="input-group-text" htmlFor="videoInput">
            <button
              type="submit"
              className="btn btn-primary"
              disabled={buttonDisabled}
            >
              Upload
            </button>
          </label>
        </div>
      </form>
    </>
  );
};

export default UploadBtn;
