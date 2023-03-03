import React, { useEffect, useRef, useState } from "react";
import axios from "axios";
import "./FileUpload.css";

const server_path = "http://localhost:8001";

type FileInfoType = {
  name: string;
  type: string;
  size: number;
};

type FileProgressType = {
  [key: string]: number;
};

const FileUpload = () => {
  const hiddenFileInput = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<FileList>();
  const [filesProgress, setFilesProgress] = useState<FileProgressType>({});

  const onChangeUploadFile = (e: any) => {
    setFiles(e.target.files);
  };

  const onDragOver = (e: any) => {
    /** This avoids the browser to open another tab */
    e.preventDefault();
  };

  const onDrop = (e: any) => {
    /** This avoids the browser to open another tab */
    e.preventDefault();
    const dt_files = e.dataTransfer.files;
    let file_list = dt_files;
    setFiles(file_list);
  };

  const onClickUpload = (e: any) => {
    if (hiddenFileInput.current) {
      hiddenFileInput.current.click();
    }
  };

  const getCSRFToken = () => {
    const url = `${server_path}/get_token/`;
    return fetch(url)
      .then((response) => response.json())
      .then((data) => data.csrfToken);
  };

  const getPercentageLoaded = (filename: string) => {
    const size =
      filesProgress[`_${filename}`] > 100 ? 100 : filesProgress[`_${filename}`];
    return { width: `${size}%` };
  };

  const sendFile = (data: any, fileinfo: FileInfoType, csrfToken: string) => {
    const url = `${server_path}/upload_file_post/`;
    const config = {
      onUploadProgress: (progressEvent: any) => {
        const loaded = progressEvent.loaded;
        const progress = JSON.parse(JSON.stringify(filesProgress));
        progress[`_${fileinfo.name}`] = Math.ceil(
          (loaded * 100) / fileinfo.size
        );
        if (progress[`_${fileinfo.name}`] >= 100) {
          delete progress[fileinfo.name];
        }
        setFilesProgress(progress);
      },
      headers: {
        "X-CSRFToken": csrfToken,
      },
    };
    return axios.post(url, data, config);
  };

  const saveFiles = () => {
    if (files && files.length > 0) {
      let progress = {};
      for (let file of files) {
        progress = { ...progress, ...{ [`_${file.name}`]: 0 } };
        saveFile(file);
      }
      setFilesProgress(progress);
    }
  };

  const saveFile = (file: File) => {
    getCSRFToken().then((csrfToken: any) => {
      const fileinfo = { name: file.name, type: file.type, size: file.size };
      const fileUpload = new FormData();
      fileUpload.append("filename", fileinfo.name);
      fileUpload.append("size", String(fileinfo.size));
      fileUpload.append("file", file, fileinfo.name);
      fileUpload.append("csrfmiddlewaretoken", csrfToken);
      sendFile(fileUpload, fileinfo, csrfToken).catch((error) => {
        console.error("Error:", error);
      });
    });
  };

  useEffect(() => {
    if (files && files.length > 0) {
      saveFiles();
    }
  }, [files]);

  return (
    <fieldset className="drag-n-drop">
      <h4 className="lbl lbl-main">Upload your files</h4>
      <input
        className="display-none"
        type="file"
        name="file"
        multiple={true}
        onChange={onChangeUploadFile}
        ref={hiddenFileInput}
      />
      <div
        className="droppable-area"
        onDrop={onDrop}
        onDragOver={onDragOver}
        onClick={onClickUpload}
      >
        <h6 className="lbl lbl-drop">Drag and drop or click to browse files</h6>
      </div>
      <div
        className={`file-list ${files && files.length > 3 && "show-scroll"}`}
      >
        {files &&
          files.length > 0 &&
          Array.from(files).map((file, index) => {
            return (
              <div key={`file-name-${index}`} className="file">
                <div className="file-loaded">
                  <div style={getPercentageLoaded(file.name)}></div>
                </div>
                <div className="filename">{file.name}</div>
              </div>
            );
          })}
      </div>
    </fieldset>
  );
};

export default FileUpload;
