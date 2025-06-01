import './App.css';
import React, {useState, useEffect} from 'react'
import api from './api'
import Table from 'react-bootstrap/Table';
import Form from 'react-bootstrap/Form';
import Button from 'react-bootstrap/Button';

const defaultFormData = {
  name: '',
  type: 'foo-bot',
  status: 'IDLE',
  description: '',
};

const App = () => {
  const [robots, setStateRobots] = useState([]); // State to hold the list of current robots. setStateRobots is the function to update this state.
  const [formData, setStateFormData] = useState(defaultFormData);
  const [error, setStateError] = useState(null); // State to hold error messages.

  const fetchRobots = async () => {
    try {
      const response = await api.get('/api/v1/robots'); // Fetch robots from the BE API.
      setStateRobots(response.data.data.robots || []); // Update the robots state.
      setStateError(null); // Clear any previous error
    } catch (err) {
      setStateError(err.response?.data?.error || err.message || 'Failed to fetch robots.');
    }
  };

  useEffect(() => { // React hook to fetch robots when the component mounts (Page load).
    fetchRobots();
  }, []);

  const handleInputChange = (event) => {
    const value = event.target.type === 'checkbox' ? event.target.checked : event.target.value;
    setStateFormData({
      ...formData,
      [event.target.name]: value,
    });
  }

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    try {
      await api.post('/api/v1/robots', formData); // Post the form data to the BE API to create a new robot.
      fetchRobots(); // Fetch the updated list of robots after form submission.
      setStateFormData(defaultFormData); // Reset the form data to default after submission.
      setStateError(null); // Clear any previous error
    } catch (err) {
      setStateError(err.response?.data?.error || err.message || 'Failed to add robot.');
    }
  };

  return (
    <div className="bg-light min-vh-100" style={{ padding: '32px' }}>
      {/* Navbar */}
      <nav className='navbar navbar-dark bg-primary rounded-4 mb-4'>
        <div className='container-fluid'>
          <a className='navbar-brand' href='/'>
            Robot Dashboard
          </a>
        </div>
      </nav>

      {/* Error Alert */}
      {error && (
        <div className="container mb-4">
          <div className="alert alert-danger rounded-4 shadow-sm text-center" role="alert">
            {error}
          </div>
        </div>
      )}

      {/* Form Section */}
      <div className='container my-5'>
        <div className='row justify-content-center'>
          <div className='col-md-6'>
            <div className='card shadow rounded-4'>
              <div className='card-header bg-primary text-white text-center rounded-top-4'>
                <h4 className='mb-0'>Add a New Robot</h4>
              </div>
              <div className='card-body bg-light rounded-bottom-4'>
                <Form onSubmit={handleFormSubmit}>
                  <div className='row g-3'>
                    <div className='col-12'>
                      <Form.Group controlId='name'>
                        <Form.Label>Name</Form.Label>
                        <Form.Control
                          type='text'
                          name='name'
                          className='rounded-pill shadow-sm'
                          value={formData.name}
                          onChange={handleInputChange}
                          required
                        />
                      </Form.Group>
                    </div>
                    <div className='col-12'>
                      <Form.Group controlId='type'>
                        <Form.Label>Type</Form.Label>
                        <Form.Select
                          name='type'
                          className='rounded-pill shadow-sm'
                          value={formData.status}
                          onChange={handleInputChange}
                        >
                          <option value='foo-bot'>foo-bot</option>
                          <option value='bar-bot'>bar-bot</option>
                        </Form.Select>
                      </Form.Group>
                    </div>
                    <div className='col-12'>
                      <Form.Group controlId='status'>
                        <Form.Label>Status</Form.Label>
                        <Form.Select
                          name='status'
                          className='rounded-pill shadow-sm'
                          value={formData.status}
                          onChange={handleInputChange}
                        >
                          <option value='IDLE'>IDLE</option>
                          <option value='ACTIVE'>ACTIVE</option>
                        </Form.Select>
                      </Form.Group>
                    </div>
                    <div className='col-12'>
                      <Form.Group controlId='description'>
                        <Form.Label>Description</Form.Label>
                        <Form.Control
                          type='text'
                          name='description'
                          className='rounded-pill shadow-sm'
                          value={formData.description}
                          onChange={handleInputChange}
                        />
                      </Form.Group>
                    </div>
                    <div className='col-12'>
                      <Button type='submit' variant='success' className='w-100 rounded-pill shadow-sm fw-bold'>
                        <span role='img' aria-label='robot'>🤖</span> Add Robot
                      </Button>
                    </div>
                  </div>
                </Form>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Table Section */}
      <div className='container'>
        <div className='card shadow rounded-4 my-5'>
          <div className='card-header bg-primary text-white text-center rounded-top-4'>
            <h2 className='mb-0'>Robot Inventory</h2>
          </div>
          <div className='card-body bg-light rounded-bottom-4 p-4'>
            <Table striped bordered hover responsive className='align-middle' style={{ borderCollapse: 'separate', borderSpacing: 0 }}>
              <thead className='table-dark'>
                <tr>
                  <th className='text-start'>ID</th>
                  <th className='text-start'>Name</th>
                  <th className='text-start'>Type</th>
                  <th className='text-start'>Status</th>
                  <th className='text-start'>Description</th>
                </tr>
              </thead>
              <tbody>
                {robots.map((item) => (
                  <tr key={item.id}>
                    <td>{item.id}</td>
                    <td>{item.name}</td>
                    <td>{item.type}</td>
                    <td>{item.status}</td>
                    <td>{item.description}</td>
                  </tr>
                ))}
              </tbody>
            </Table>
          </div>
        </div>
      </div>
    </div>
  )

}

export default App;
