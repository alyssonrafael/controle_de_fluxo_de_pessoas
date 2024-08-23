import React, { useEffect, useState } from 'react';
import axios from 'axios';

const Dashboard = () => {
    const [status, setStatus] = useState({ peopleIn: 0, peopleOut: 0, peopleInside: 0 });

    const fetchData = async () => {
        try {
            const response = await axios.get('http://localhost:3001/api/status');
            setStatus(response.data);
        } catch (error) {
            console.error('Erro ao buscar os dados:', error);
        }
    };

    useEffect(() => {
        fetchData();
        const interval = setInterval(fetchData, 1000); // Atualiza a cada segundo
        return () => clearInterval(interval);
    }, []);

    return (
        <div>
            <h1>Dashboard de Contagem de Pessoas</h1>
            <p>Entradas: {status.peopleIn}</p>
            <p>Saídas: {status.peopleOut}</p>
            <p>Pessoas Dentro: {status.peopleInside}</p>
        </div>
    );
};

export default Dashboard;
