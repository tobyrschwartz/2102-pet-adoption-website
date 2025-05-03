import React, { useEffect, useState } from 'react';
import { useUser } from '../context/UserContext';
import { useNavigate } from 'react-router-dom';
import { QuestionType } from './AdminApplications';

interface Question {
    id: number;
    text: string;
    type: QuestionType;
    options?: string[];
}

const Questionnaire: React.FC = () => {
    const { user } = useUser();
    const navigate = useNavigate();
    const [hasSubmitted, setHasSubmitted] = useState<boolean | null>(false);
    const [questions, setQuestions] = useState<Question[]>([]);
    const [answers, setAnswers] = useState<Record<number, string>>({});
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (user === null) return;
        if (!user) {
          navigate('/unauthorized');
          return;
        }
      
        const checkSubmission = async () => {
          const res = await fetch('http://localhost:5000/api/questionnaires/hasOpen', {
            method: 'GET',
            credentials: 'include',
          });
      
          if (!res.ok) {
            console.error('Failed to check submission status.');
            return;
          }
      
          const data = await res.json();
          setHasSubmitted(data.has_open); 
      
          if (!data.has_open) {
            const questionsRes = await fetch('http://localhost:5000/api/questionnaires', {
              method: 'GET',
              credentials: 'include',
            });
      
            if (!questionsRes.ok) {
              console.error('Failed to load questions.');
              return;
            }
      
            const questionsData = await questionsRes.json();
            const formattedQuestions = questionsData.map((q: any) => ({
              id: q.id,
              text: q.text,
              type: q.type.toLowerCase(),
              options: q.options || [],
            }));
      
            setQuestions(formattedQuestions);
          }
      
          setLoading(false);
        };
      
        checkSubmission();
      }, [user]);      

    const handleInputChange = (questionId: number, value: string) => {
        setAnswers(prev => ({ ...prev, [questionId]: value }));
    };

    const handleSubmit = async () => {
        if (!user) return;
      
        const formattedAnswers = Object.entries(answers).map(([questionId, answerText]) => ({
          question_id: parseInt(questionId),
          answer_text: answerText,
        }));
      
        try {
          const res = await fetch("http://localhost:5000/api/questionnaires/submit", {
            method: "POST",
            headers: {
              "Content-Type": "application/json",
            },
            credentials: "include",
            body: JSON.stringify({ answers: formattedAnswers }),
          });
      
          const result = await res.json();
      
          if (res.ok) {
            alert("Submitted successfully!");
            navigate("/pets");
          } else {
            alert(`Error: ${result.error}`);
          }
        } catch (err) {
          console.error("Submit error:", err);
          alert("Something went wrong. Try again later.");
        }
      };
      

    if (loading) {
        return <div>Loading questions...</div>;
    }

    if (hasSubmitted) {
        return (
          <div style={{ textAlign: 'center', padding: '2rem' }}>
            <h2>You’ve already completed the questionnaire ✅</h2>
          </div>
        );
    }

    return (
        <div style={{ padding: '2rem', maxWidth: '700px', margin: 'auto' }}>
            <h1 style={{ fontSize: '2rem', marginBottom: '2rem' }}>Questionnaire</h1>
            <form 
            onSubmit={(e) => { e.preventDefault(); handleSubmit(); }}>
                <ul style={{ listStyle: 'none', padding: 0 }}>
                    {questions.map((question) => (
                        <li key={question.id} style={{ marginBottom: '2rem' }}>
                            <p style={{ fontWeight: 'bold' }}>{question.text}</p>
                            {question.type === QuestionType.TEXT && (
                                <input
                                    type="text"
                                    value={answers[question.id] || ''}
                                    onChange={(e) => handleInputChange(question.id, e.target.value)}
                                    placeholder="Your answer"
                                    style={{
                                        padding: '0.75rem',
                                        borderRadius: '8px',
                                        border: '1px solid #ccc',
                                        fontSize: '1rem',
                                        width: '100%',
                                        boxSizing: 'border-box',
                                    }}
                                />
                            )}
                            {question.type === QuestionType.MULTIPLE_CHOICE && (
                                <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem' }}>
                                    {question.options?.map((option) => (
                                        <label key={option}>
                                            <input
                                            type="radio"
                                            name={`question-${question.id}`}
                                            value={option}
                                            checked={answers[question.id] === option}
                                            onChange={() => handleInputChange(question.id, option)}
                                            style={{ marginRight: '0.5rem' }}
                                            />
                                            {option}
                                        </label>
                                    ))}
                                </div>
                            )}
                        </li>
                    ))}
                </ul>
                <button
                    type="submit"
                    style={{
                        padding: '0.75rem 1.5rem',
                        fontSize: '1rem',
                        backgroundColor: '#28a745',
                        color: 'white',
                        border: 'none',
                        borderRadius: '8px',
                        cursor: 'pointer',
                    }}
                >
                    Submit
                </button>
            </form>
        </div>
    );
};

export default Questionnaire;