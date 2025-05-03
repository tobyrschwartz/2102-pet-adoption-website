import React, { useState, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useUser } from "../context/UserContext";

enum QuestionType {
  TEXT = "text",
  MULTIPLE_CHOICE = "multiple_choice",
}

interface Question {
  id: number;
  text: string;
  type: QuestionType;
  options?: string[];
}

const containerStyle: React.CSSProperties = {
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  overflowY: 'auto',
  padding: '2rem',
  minHeight: '100vh', 
  boxSizing: 'border-box',
};

const headerStyle: React.CSSProperties = {
  fontSize: '2rem',
  fontWeight: 'bold',
  marginBottom: '2rem',
};

const inputStyle: React.CSSProperties = {
  padding: '0.75rem',
  borderRadius: '8px',
  border: '1px solid #ccc',
  fontSize: '1rem',
  width: '100%',
  maxWidth: '400px',
  boxSizing: 'border-box',
};

const buttonStyle: React.CSSProperties = {
  padding: '0.75rem 1.5rem',
  borderRadius: '8px',
  backgroundColor: '#007BFF',
  color: 'white',
  fontSize: '1rem',
  border: 'none',
  cursor: 'pointer',
};

const saveButtonStyle: React.CSSProperties = {
  ...buttonStyle,
  backgroundColor: '#28a745',
};

const deleteButtonStyle: React.CSSProperties = {
  ...buttonStyle,
  backgroundColor: '#dc3545',
};

const editButtonStyle: React.CSSProperties = {
  ...buttonStyle,
  backgroundColor: '#ffc107',
  color: 'black',
};

const AdminApplications: React.FC = () => {
  const { user, isLoading } = useUser();
  const isAdmin = user && user.role === 3;
  const navigate = useNavigate();

  const [questions, setQuestions] = useState<Question[]>([]);
  const [newQuestion, setNewQuestion] = useState<string>("");
  const [newOption, setNewOption] = useState<string>("");
  const [editingQuestionId, setEditingQuestionId] = useState<number | null>(null);
  const [editingText, setEditingText] = useState<string>("");
  const [questionType, setQuestionType] = useState<QuestionType>(QuestionType.TEXT);
  const [editingOptions, setEditingOptions] = useState<string[]>([]);
  const [saving, setSaving] = useState(false);

  useEffect(() => {
    if (isLoading) return;
    if (!isAdmin) {
      navigate('/unauthorized');
      return;
    }
  
    const loadQuestions = async () => {
      try {
      const res = await fetch('http://localhost:5000/api/questionnaires', {
        method: 'GET',
        credentials: 'include',
      });
    
      if (res.ok) {
        const data = await res.json();
        const formattedQuestions = data.map((q: any) => ({
        id: q.id,
        text: q.text,
        type: q.type === "TEXT" ? QuestionType.TEXT : QuestionType.MULTIPLE_CHOICE,
        options: q.options || [],
        }));
        setQuestions(formattedQuestions);
      } else {
        console.error('Failed to load questions.');
      }
      } catch (error) {
      console.error('Error fetching questions:', error);
      }
    };
  
    loadQuestions();
  }, [user, isAdmin]);

  const handleAddQuestion = () => {
    if (newQuestion.trim() === "") return;
    const newId = questions.length > 0 ? questions[questions.length - 1].id + 1 : 1;
    const newQuestionObj: Question = {
      id: newId,
      text: newQuestion,
      type: questionType,
      options: questionType === QuestionType.MULTIPLE_CHOICE ? [] : undefined,
    };
    setQuestions([...questions, newQuestionObj]);
    setNewQuestion("");
    setQuestionType(QuestionType.TEXT);
  };

  const handleDeleteQuestion = (id: number) => {
    setQuestions(questions.filter((q) => q.id !== id));
  };

  const handleEditQuestion = (id: number) => {
    const questionToEdit = questions.find((q) => q.id === id);
    if (questionToEdit) {
      setEditingQuestionId(id);
      setEditingText(questionToEdit.text);
      setEditingOptions(questionToEdit.options || []);
    }
  };

  const handleSaveEdit = () => {
    setQuestions(
      questions.map((q) =>
        q.id === editingQuestionId
          ? { ...q, text: editingText, options: editingOptions }
          : q
      )
    );
    setEditingQuestionId(null);
    setEditingText("");
    setEditingOptions([]);
  };

  const handleAddOption = () => {
    if (newOption.trim() === "") return;
    setEditingOptions([...editingOptions, newOption]);
    setNewOption("");
  };

  const handleDeleteOption = (index: number) => {
    setEditingOptions(editingOptions.filter((_, i) => i !== index));
  };

  const handleSaveQuestions = async () => {
    setSaving(true);
    try {
      const res = await fetch("http://localhost:5000/api/questionnaires", {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        credentials: "include",
        body: JSON.stringify({ questions }),
      });

      if (res.ok) {
        alert("Questions saved successfully!");
      } else {
        alert("Failed to save questions.");
      }
    } catch (error) {
      console.error("Error saving questions:", error);
    } finally {
      setSaving(false);
    }
  };

  return (
    <div style={{ height: '90vh', overflowY: 'auto' }}>
      <div style={containerStyle}>
        <h1 style={headerStyle}>Manage Application Questions</h1>

        {/* Add new question */}
        <div style={{ display: 'flex', gap: '1rem', marginBottom: '2rem', flexWrap: 'wrap', justifyContent: 'center' }}>
          <input
            type="text"
            placeholder="Enter a new question"
            value={newQuestion}
            onChange={(e) => setNewQuestion(e.target.value)}
            style={inputStyle}
          />
          <select
            value={questionType}
            onChange={(e) => setQuestionType(e.target.value as QuestionType)}
            style={inputStyle}
          >
            <option value={QuestionType.TEXT}>Text</option>
            <option value={QuestionType.MULTIPLE_CHOICE}>Multiple Choice</option>
          </select>
          <button onClick={handleAddQuestion} style={buttonStyle}>
            Add
          </button>
        </div>

        {/* List of questions */}
        <ul style={{ width: '100%', maxWidth: '600px', overflowY: 'auto', maxHeight: '60vh', padding: 0 }}>
          {questions.map((question) => (
            <li key={question.id} style={{
              border: '1px solid #ccc',
              borderRadius: '8px',
              padding: '1rem',
              marginBottom: '1rem',
              backgroundColor: '#2b3e5c'
            }}>
              {editingQuestionId === question.id ? (
                <>
                  <input
                    type="text"
                    value={editingText}
                    onChange={(e) => setEditingText(e.target.value)}
                    style={{ ...inputStyle, marginBottom: '0.5rem' }}
                  />
                  {question.type === QuestionType.MULTIPLE_CHOICE && (
                    <div style={{ display: 'flex', flexDirection: 'column', gap: '0.5rem', marginBottom: '0.5rem' }}>
                      <h4 style={{ fontWeight: 'bold' }}>Options:</h4>
                      {editingOptions.map((option, index) => (
                        <div key={index} style={{ display: 'flex', alignItems: 'center', gap: '0.5rem' }}>
                          <span>{option}</span>
                          <button
                            onClick={() => handleDeleteOption(index)}
                            style={deleteButtonStyle}
                          >
                            Delete
                          </button>
                        </div>
                      ))}
                      <div style={{ display: 'flex', gap: '0.5rem' }}>
                        <input
                          type="text"
                          placeholder="Add option"
                          value={newOption}
                          onChange={(e) => setNewOption(e.target.value)}
                          style={inputStyle}
                        />
                        <button onClick={handleAddOption} style={saveButtonStyle}>
                          Add Option
                        </button>
                      </div>
                    </div>
                  )}
                  <div style={{ display: 'flex', gap: '1rem' }}>
                    <button onClick={handleSaveEdit} style={saveButtonStyle}>
                      Save
                    </button>
                    <button onClick={() => setEditingQuestionId(null)} style={buttonStyle}>
                      Cancel
                    </button>
                  </div>
                </>
              ) : (
                <>
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <span style={{ fontWeight: 'bold' }}>{question.text}</span>
                    <div style={{ display: 'flex', gap: '0.5rem' }}>
                      <button
                        onClick={() => handleEditQuestion(question.id)}
                        style={editButtonStyle}
                      >
                        Edit
                      </button>
                      <button
                        onClick={() => handleDeleteQuestion(question.id)}
                        style={deleteButtonStyle}
                      >
                        Delete
                      </button>
                    </div>
                  </div>
                  {question.type === QuestionType.MULTIPLE_CHOICE && (
                    <ul style={{ marginTop: '0.5rem', paddingLeft: '1rem' }}>
                      {question.options?.map((option, index) => (
                        <li key={index} style={{ fontSize: '0.9rem', color: '#fff00' }}>
                          {option}
                        </li>
                      ))}
                    </ul>
                  )}
                </>
              )}
            </li>
          ))}
        </ul>

        {/* Save all questions */}
        <button
          onClick={handleSaveQuestions}
          disabled={saving}
          style={{ ...saveButtonStyle, marginTop: '2rem' }}
        >
          {saving ? "Saving..." : "Save All Changes"}
        </button>
      </div>
    </div>
  );
};

export default AdminApplications;
export type { Question };
export { QuestionType };

