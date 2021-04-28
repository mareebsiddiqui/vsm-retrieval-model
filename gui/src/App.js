import React, { useEffect, useState } from 'react';
import './App.css';
import Highlighter from 'react-highlight-words';

function App() {

  const [docIndex, setDocIndex] = useState({});

  const [input, setInput] = useState();

  const [results, setResults] = useState([]);

  const [status, setStatus] = useState("No results.");

  const [showDocument, setShowDocument] = useState(false);

  const [selectedDocId, setSelectedDocId] = useState();
  const [selectedDoc, setSelectedDoc] = useState({});

  // const SERVER_URL = 'http://localhost:5000/';
  const SERVER_URL = 'http://100.24.236.194:5000/';

  useEffect(() => {
    console.log("abcd")
    fetch(`${SERVER_URL}/doc_index`)
    .then(res => res.json())
    .then(res_json => {
      setDocIndex(res_json);
    });
  }, []);

  function camelize(str) {
    if(str) {
      let result = str.replace( /([A-Z])/g, "$1" );
      let finalResult = result.charAt(0).toUpperCase() + result.slice(1);
      return finalResult;
    }
  }

  function handleKeyDown(event) {
    if (event.key === 'Enter') {
      if(input) {
        setStatus("Loading...");
        setResults([]);
        fetch(`${SERVER_URL}/query?query=`+input)
        .then(res => res.json())
        .then(res_json => {
          console.log(res_json);
          setResults(res_json.results);
          setStatus("No results.");
        })
        .catch(err => {
          console.log(err);
        })
      } else {
        setResults([]);
        setShowDocument(false);
        setSelectedDocId();
        setSelectedDoc({});
      }
    }
  }

  useEffect(() => {
    if(selectedDocId) {
      fetch(`${SERVER_URL}/document?doc_id=`+selectedDocId)
      .then(res => res.json())
      .then(res_json => {
        setSelectedDoc(res_json);
      })
      .catch(err => {
        console.log(err);
      })
    }
  }, [selectedDocId]);

  function renderResults() {
    if(results.length > 0) {
      return results.map(doc_id => {
        return (
          <div className="result mb-4">
            <p className="lead text-white" href="#">
              {doc_id}.
              <a
                href="#" 
                className="text-white" 
                onClick={(e) => {
                  e.preventDefault()
                  setShowDocument(true);
                  setSelectedDocId(doc_id);
                  setSelectedDoc({});
                }}>
                  {camelize(docIndex[doc_id])}
              </a>
            </p>
          </div>
        );
      })
    } else {
      return <p className="text-white">{status}</p>
    }
  }

  return (
    <div className="App">
      <header className="App-header">
        <h6 className="text-muted">M. Areeb Siddiqui - k181062</h6>
        <h1 className="display-4">
          Short Stories
        </h1>
        {!showDocument && (
          <div className="col-lg-8 content">
            <div className="form-floating mb-3">
              <input type="text" className="form-control" value={input} id="floatingInput" onKeyDown={handleKeyDown} onChange={e => setInput(e.target.value)} autoFocus />
              <label style={{color: "#282c34"}} htmlFor="floatingInput">query + enter</label>
            </div>
            <hr/>
            {renderResults()}
          </div>
        )}
        {showDocument && selectedDoc.doc_name && (
          <>
            <a className="text-white" href="#" onClick={(e) => {
              e.preventDefault();
              setShowDocument(false);
            }}>Back</a>
            <h3>
              {selectedDoc.doc_name}  
            </h3>
            <div className="col-lg-10 content">
              <p style={{textAlign: "justify"}}>
                {selectedDoc.doc}
              </p>
            </div>
          </>
        )}
        {showDocument && !selectedDoc.doc_name && (
          <p>Loading..</p>
        )}
      </header>
    </div>
  );
}

export default App;
