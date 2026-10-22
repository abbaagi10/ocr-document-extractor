import { useState, useEffect, useRef } from 'react'

function App() {
  const [file, setFile] = useState(null)
  const [previewUrl, setPreviewUrl] = useState(null)
  const [status, setStatus] = useState('idle') // idle, uploading, processing, completed, error
  const [docId, setDocId] = useState(null)
  const [result, setResult] = useState({ json: null, text: '' })
  
  const fileInputRef = useRef(null)
  const API_URL = "http://localhost:8000/api/documents/"

  const handleFileChange = (e) => {
    if (e.target.files && e.target.files.length > 0) {
      const selectedFile = e.target.files[0]
      setFile(selectedFile)
      setPreviewUrl(URL.createObjectURL(selectedFile))
      setStatus('idle')
      setResult({ json: null, text: '' })
    }
  }

  const handleUpload = async () => {
    if (!file) return

    setStatus('uploading')
    const formData = new FormData()
    formData.append("image", file)

    try {
      const response = await fetch(API_URL, { method: 'POST', body: formData })
      if (!response.ok) {
        const errorDetail = await response.json()
        alert("Erreur serveur : " + JSON.stringify(errorDetail))
        setStatus('error')
        return
      }
      
      const data = await response.json()
      setDocId(data.id)
      setStatus('processing')
    } catch (error) {
      alert("Erreur de connexion à l'API. Docker tourne-t-il ?")
      setStatus('error')
    }
  }

  useEffect(() => {
    let interval;
    if (status === 'processing' && docId) {
      interval = setInterval(async () => {
        try {
          const response = await fetch(`${API_URL}${docId}/`)
          const data = await response.json()

          if (data.status === 'completed' || data.status === 'error') {
            setStatus(data.status)
            setResult({
              json: data.structured_data,
              text: data.extracted_text
            })
            clearInterval(interval)
          }
        } catch (error) {
          console.error("Erreur de polling", error)
          setStatus('error')
          clearInterval(interval)
        }
      }, 2000)
    }
    return () => clearInterval(interval)
  }, [status, docId])

  return (
    <div className="bg-gray-100 min-h-screen p-10 font-sans">
      <div className="max-w-4xl mx-auto bg-white p-8 rounded-xl shadow-lg">
        <h1 className="text-3xl font-bold text-gray-800 mb-2">Extracteur de Documents IA</h1>
        <p className="text-gray-500 mb-8">Architecture Full-Stack Asynchrone (React + Django + Celery + Gemini)</p>

        {/* Zone d'upload */}
        <div className="border-4 border-dashed border-blue-200 rounded-lg p-10 text-center bg-blue-50 transition hover:bg-blue-100">
          <input 
            type="file" 
            ref={fileInputRef} 
            className="hidden" 
            accept="image/png, image/jpeg, image/jpg"
            onChange={handleFileChange} 
          />
          <button 
            type="button" 
            onClick={() => fileInputRef.current.click()} 
            className="bg-blue-600 text-white px-6 py-3 rounded-lg font-semibold hover:bg-blue-700 transition shadow-md"
          >
            Sélectionner une image
          </button>
          
          {file && <p className="mt-4 text-gray-600 font-medium">📄 {file.name}</p>}
          
          {previewUrl && (
            <div className="mt-6 flex justify-center">
              <img src={previewUrl} alt="Aperçu" className="max-h-64 rounded-lg shadow-md border border-gray-300 object-contain" />
            </div>
          )}
        </div>

        {/* Bouton d'action */}
        {file && status === 'idle' && (
          <button 
            type="button" 
            onClick={handleUpload} 
            className="w-full mt-6 bg-green-500 text-white px-6 py-3 rounded-lg font-bold hover:bg-green-600 transition shadow-md"
          >
            Lancer l'Extraction IA
          </button>
        )}

        {/* Zone des résultats */}
        {status !== 'idle' && (
          <div className="mt-10">
            <h2 className="text-xl font-bold text-gray-800 mb-4 flex items-center">
              Statut : 
              <span className={`ml-3 px-3 py-1 text-sm rounded-full font-bold ${
                status === 'processing' || status === 'uploading' ? 'bg-yellow-100 text-yellow-800 animate-pulse' :
                status === 'completed' ? 'bg-green-100 text-green-800' :
                'bg-red-100 text-red-800'
              }`}>
                {status === 'uploading' && 'Envoi en cours...'}
                {status === 'processing' && "Analyse IA en cours..."}
                {status === 'completed' && 'Extraction Terminée !'}
                {status === 'error' && 'Erreur de traitement'}
              </span>
            </h2>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
              {/* Résultat JSON */}
              <div className="bg-gray-900 rounded-lg p-4 shadow-inner text-green-400 font-mono text-sm overflow-auto h-96">
                <h3 className="text-white mb-2 font-sans border-b border-gray-700 pb-2">Données Structurées (JSON)</h3>
                <pre>
                  {status === 'processing' || status === 'uploading' ? 'Attente de la réponse du modèle...' : 
                   result.json ? JSON.stringify(result.json, null, 2) : 
                   'Aucune donnée structurée retournée.'}
                </pre>
              </div>

              {/* Résultat Texte Brut OCR */}
              <div className="bg-gray-50 border rounded-lg p-4 text-gray-700 text-xs overflow-auto h-96">
                <h3 className="font-bold text-gray-800 mb-2 border-b pb-2">Texte Brut (Tesseract OCR)</h3>
                <pre className="whitespace-pre-wrap">
                  {status === 'processing' || status === 'uploading' ? 'Extraction des caractères en cours...' : result.text}
                </pre>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  )
}

export default App