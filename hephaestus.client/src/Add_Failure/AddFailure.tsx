import axios from 'axios';
import React, { useState } from 'react';

interface FailureData {
  failureType: string;
  name: string;
  date: string;
  potentialPrice: string;
  potentialDate: string;
  status: string;
  repairDescription: string;
}

const AddFailure: React.FC = () => {
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [failureData, setFailureData] = useState<FailureData>({
    failureType: '0',
    name: '',
    date: new Date().toISOString().slice(0, 10),
    potentialPrice: '',
    potentialDate: '',
    status: '0',
    repairDescription: ''
  });
  const [model, setModel] = useState(1);
  const [predictedPrice, setPredictedPrice] = useState<string | null>(null);

  const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement | HTMLSelectElement>) => {
    const { name, value } = e.target;
    setFailureData({ ...failureData, [name]: value });
  };

  const handleModelChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
      const newModel = parseInt(e.target.value, 10);
      setModel(newModel);
      handleRecalculateClick();
  };

    const handleRecalculateClick = () => {
      //Wywo³anie enpointa, przekazuj¹c zmienn¹ model i failureData.type
      //Zapisanie przeliczonej ceny w predictedPrice
  };

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();

      //Validation
      setError("");
      setSuccess("");
      let valid = true;
      const potentialDate = new Date(failureData.potentialDate);
      const date = new Date(failureData.date);
      if (parseInt(failureData.potentialPrice) < 0) {
          setError("The price can't be lower than 0.");
          valid = false;
      }
      else if (potentialDate < date) {
          setError("Potential Date can't be earlier than Date.");
          valid = false;
      }

      if (valid) {
          // Convert string values to numbers
          const convertedData = {
              ...failureData,
              failureType: parseInt(failureData.failureType),
              status: parseInt(failureData.status)
          };

          try {
              const response = await axios.post(
                  'https://localhost:7292/add-failure',
                  convertedData
              );

              console.log('Server response:', response.data);

              // Clear form fields after successful submission
              setFailureData({
                  failureType: '0',
                  name: '',
                  date: new Date().toISOString().slice(0, 10),
                  potentialPrice: '',
                  potentialDate: '',
                  status: '0',
                  repairDescription: ''
              });
              setSuccess("Failure added successfully.");
          } catch (error) {
              console.error('Error occurred:', error);
          }
      }
  };


  return (
    <div>
      <h2>Failure Form</h2>
      <form onSubmit={handleSubmit}>
      <label>
          Failure Type: 
          <select
            name="failureType"
            value={failureData.failureType}
            onChange={handleChange}
            required
          >
            <option value="0">Low</option>
            <option value="1">Mild</option>
            <option value="2">High</option>
            <option value="3">Critical</option>
          </select>
        </label>
        <br />
        <label>
          Name:
          <input
            type="text"
            name="name"
            value={failureData.name}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Date:
          <input
            type="date"
            name="date"
            value={failureData.date}
            onChange={handleChange}
            disabled
            required
          />
        </label>
        <br />
        <label>
          Model:
          <select
            name="model"
            value={model}
            onChange={handleModelChange}
            required
          >
            <option value="1">Model1</option>
            <option value="2">Model2</option>
            <option value="3">Model3</option>
            <option value="4">Model4</option>
            <option value="5">Model5</option>
          </select>
        </label>
              <br />
              <label>Predicted Price: {predictedPrice ? predictedPrice : '0'} </label><button type="button" onClick={handleRecalculateClick}>Recalculate</button>
        <br />
        <label>
          Potential Price:
          <input
            type="number"
            name="potentialPrice"
            value={failureData.potentialPrice}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Potential Date:
          <input
            type="date"
            name="potentialDate"
            value={failureData.potentialDate}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        <label>
          Status:
          <select
            name="status"
            value={failureData.status}
            onChange={handleChange}
            required
          >
            <option value="0">New</option>
            <option value="1">InProgress</option>
            <option value="2">Finished</option>
            <option value="3">Unrepairable</option>
          </select>
        </label>
        <br />
        <label>
          Repair Description:
          <textarea
            name="repairDescription"
            value={failureData.repairDescription}
            onChange={handleChange}
            required
          />
        </label>
        <br />
        {error && <div style={{ color: 'red' }}>{error}</div>}
        <button type="submit">Submit</button>
      </form>
          {success && <div style={{ color: 'green' }}>{success}</div>}
    </div>
  );
};

export default AddFailure;
