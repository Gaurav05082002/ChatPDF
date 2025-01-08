import React from 'react';

import FileUpload from '../components/FileUpload';
import AskQuestion from '../components/AskQuestion';

function Landing() {
  return (
    <div>
      <h1>Chat with PDF using Gemini 💁</h1>
      <FileUpload />
      <AskQuestion />
    </div>
  );
}

export default Landing;
