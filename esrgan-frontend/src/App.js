import React, { useState, useRef } from 'react';
import { Container, Typography, Button, Box, Grid, Card, CardContent } from '@mui/material';
import Webcam from 'react-webcam';
import './App.css';

function App() {
  const [image, setImage] = useState(null);
  const [videoCaptured, setVideoCaptured] = useState(null);
  const [file, setFile] = useState(null); // Track the file object
  const webcamRef = useRef(null); // Ref for Webcam

  // Handle image upload
  const handleImageUpload = (e) => {
    const uploadedFile = e.target.files[0];
    if (uploadedFile) {
      setFile(uploadedFile); // Store the file
      const reader = new FileReader();
      reader.onloadend = () => {
        setImage(reader.result); // Set base64 string for display
      };
      reader.readAsDataURL(uploadedFile);
    }
  };

  // Handle video capture
  const captureVideo = () => {
    if (webcamRef.current) {
      const imageSrc = webcamRef.current.getScreenshot();
      setVideoCaptured(imageSrc);
    }
  };

  // Enhance Image with ESRGAN
  const enhanceImage = async () => {
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch("http://localhost:5000/enhance-image", {
        method: "POST",
        body: formData,
      });

      // Check if the response is ok
      if (response.ok) {
        const result = await response.blob();
        const url = URL.createObjectURL(result);
        setImage(url);  // Update image with enhanced result
      } else {
        throw new Error('Failed to enhance the image');
      }
    } catch (error) {
      console.error('Error enhancing image', error);
      alert('There was an error enhancing the image. Please try again.');
    }
  };

  return (
    <Container>
      <Typography variant="h3" align="center" gutterBottom>
        Super Resolution
      </Typography>
      <Grid container spacing={2} justifyContent="center">
        {/* Webcam Section */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h5">Capture Live Video</Typography>
              <Webcam
                audio={false}
                ref={webcamRef}
                screenshotFormat="image/jpeg"
                width="100%"
                videoConstraints={{ facingMode: 'user' }}
              />
              <Button
                variant="contained"
                color="primary"
                onClick={captureVideo}
                fullWidth
              >
                Capture Video Frame
              </Button>
              {videoCaptured && <img src={videoCaptured} alt="Captured Frame" width="100%" />}
            </CardContent>
          </Card>
        </Grid>

        {/* Image Upload Section */}
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h5">Upload Image for Super-Resolution</Typography>
              <input type="file" onChange={handleImageUpload} />
              {image && (
                <Box mt={2}>
                  <img src={image} alt="Uploaded" style={{ maxWidth: '100%' }} />
                </Box>
              )}
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Button to Trigger ESRGAN Backend Call */}
      <Box mt={3} display="flex" justifyContent="center">
        <Button
          variant="contained"
          color="secondary"
          onClick={enhanceImage}  // Trigger the enhancement
        >
          Enhance Image with ESRGAN
        </Button>
      </Box>
    </Container>
  );
}

export default App;
