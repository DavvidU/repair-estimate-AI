import React, { useState, useEffect } from 'react';
import axios from 'axios';
import mapFailureTypeToText from '../Mappers/MapFailureTypeToText'
import mapStatusToText from '../Mappers/MapStatusToText'
import mapDateFormat from '../Mappers/MapDateFormat'

interface Failure {
  failureType: number;
  name: string;
  date: string;
  potentialPrice: number;
  potentialDate: string;
  status: number;
  repairDescription: string;
}

const FailureList: React.FC = () => {
  const [failures, setFailures] = useState<Failure[]>([]);

  useEffect(() => {
    const fetchFailures = async () => {
      try {
        const response = await axios.get<Failure[]>('https://localhost:7292/failures');
        setFailures(response.data);
      } catch (error) {
        console.error('Error fetching failures:', error);
      }
    };

    fetchFailures();
  }, []); // Empty dependency array ensures that effect runs only once on component mount

  return (
    <div>
      <h2>Failure list</h2>
          <table>
              <thead>
                    <tr>
                        <th>ID</th>
                        <th>Name</th>
                        <th>Failure Type</th>
                        <th>Date</th>
                        <th>Potential Price</th>
                        <th>Potential Date</th>
                        <th>Status</th>
                        <th>Repair Description</th>
                        <th>Action</th>
                    </tr>
              </thead>
              <tbody>
                  {failures.map((failure, index) => (
                      <tr key={index}>
                          <td>{failure.id}</td>
                          <td>{failure.name}</td>
                          <td>{mapFailureTypeToText(failure.failureType)}</td>
                          <td>{mapDateFormat(failure.date)}</td>
                          <td>{failure.potentialPrice}</td>
                          <td>{mapDateFormat(failure.potentialDate)}</td>
                          <td>{mapStatusToText(failure.status)}</td>
                          <td>{failure.repairDescription}</td>
                          <td><a href={`/failure/details/${failure.id}`}><button>Failure details</button></a></td>
                      </tr>
                  ))}
              </tbody>
          </table>
    </div>
  );
};

export default FailureList;
