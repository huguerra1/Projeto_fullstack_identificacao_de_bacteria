import { useState } from 'react';
import { Container, Row, Col, Card, Form, Button, Spinner, Alert } from 'react-bootstrap';
import { analyzeSample } from '../services/api';

export function Home() {
  // Estados para arquivos
  const [sampleRaw, setSampleRaw] = useState<File | null>(null);
  const [sampleHdr, setSampleHdr] = useState<File | null>(null);
  const [darkRaw, setDarkRaw] = useState<File | null>(null);
  const [darkHdr, setDarkHdr] = useState<File | null>(null);
  const [whiteRaw, setWhiteRaw] = useState<File | null>(null);
  const [whiteHdr, setWhiteHdr] = useState<File | null>(null);

  // Estados de opção
  const [snv, setSnv] = useState(false);  
  const [savgol, setSavgol] = useState(false);

  // Estados da UI
  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async () => {
    if (!sampleRaw || !sampleHdr || !darkRaw || !darkHdr || !whiteRaw || !whiteHdr) {
      setError("Por favor, selecione TODOS os 6 arquivos para calibração.");
      return;
    }
    
    setLoading(true);
    setError(null);

    try {
      const response = await analyzeSample({
        sampleRaw, sampleHdr,
        darkRaw, darkHdr,
        whiteRaw, whiteHdr,
        snv, savgol
      });

      if (response.status === 'error') {
        setError(response.message);
      } else {
        setResult(response.data);
      }
    } catch (err) {
      setError("Erro de conexão com o servidor.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container className="py-4">
      <h2 className="mb-4 text-center">Análise Hiperespectral com Calibração</h2>
      
      <Row>
        {/* COLUNA DE UPLOAD (Formulário Longo) */}
        <Col md={4}>
          <Card className="mb-3">
            <Card.Header className="bg-primary text-white">1. Amostra (Sample)</Card.Header>
            <Card.Body>
              <Form.Group className="mb-2">
                <Form.Label>Arquivo .RAW</Form.Label>
                <Form.Control type="file" onChange={(e:any) => setSampleRaw(e.target.files[0])} />
              </Form.Group>
              <Form.Group>
                <Form.Label>Arquivo .HDR</Form.Label>
                <Form.Control type="file" onChange={(e:any) => setSampleHdr(e.target.files[0])} />
              </Form.Group>
            </Card.Body>
          </Card>

          <Card className="mb-3">
            <Card.Header className="bg-dark text-white">2. Referência Escura (Dark)</Card.Header>
            <Card.Body>
              <Form.Group className="mb-2">
                <Form.Control type="file" onChange={(e:any) => setDarkRaw(e.target.files[0])} />
              </Form.Group>
              <Form.Group>
                <Form.Control type="file" onChange={(e:any) => setDarkHdr(e.target.files[0])} />
              </Form.Group>
            </Card.Body>
          </Card>

          <Card className="mb-3">
            <Card.Header className="bg-light border">3. Referência Branca (White)</Card.Header>
            <Card.Body>
              <Form.Group className="mb-2">
                <Form.Control type="file" onChange={(e:any) => setWhiteRaw(e.target.files[0])} />
              </Form.Group>
              <Form.Group>
                <Form.Control type="file" onChange={(e:any) => setWhiteHdr(e.target.files[0])} />
              </Form.Group>
            </Card.Body>
          </Card>

          <Card className="mb-3">
            <Card.Body>
              <h6>Processamento</h6>
              <Form.Check label="Aplicar SNV" checked={snv} onChange={e => setSnv(e.target.checked)} />
              <Form.Check label="Aplicar Savitzky-Golay" checked={savgol} onChange={e => setSavgol(e.target.checked)} />
              <hr/>
              <Button className="w-100" variant="success" onClick={handleSubmit} disabled={loading}>
                {loading ? <Spinner size="sm" animation="border" /> : "Processar e Calibrar"}
              </Button>
            </Card.Body>
          </Card>
        </Col>

        {/* COLUNA DE RESULTADOS */}
        <Col md={8}>
          {error && <Alert variant="danger">{error}</Alert>}
          
          {!result && !loading && (
            <div className="text-center mt-5 text-muted">
              <h4>Aguardando dados...</h4>
              <p>Carregue os arquivos ao lado para iniciar a calibração radiométrica.</p>
            </div>
          )}

          {result && (
            <Row>
              <Col md={12} className="mb-4 text-center">
                <h5>Detecção de ROI (Calibrada)</h5>
                <img src={`data:image/png;base64,${result.preview_roi}`} className="img-fluid border rounded" style={{maxHeight: '300px'}} />
              </Col>
              <Col md={6}>
                <h6 className="text-center">Espectro Médio (Bruto/Calibrado)</h6>
                <img src={`data:image/png;base64,${result.grafico_antes}`} className="img-fluid" />
              </Col>
              <Col md={6}>
                <h6 className="text-center">Espectro Médio (Processado)</h6>
                <img src={`data:image/png;base64,${result.grafico_depois}`} className="img-fluid" />
              </Col>
            </Row>
          )}
        </Col>
      </Row>
    </Container>
  );
}