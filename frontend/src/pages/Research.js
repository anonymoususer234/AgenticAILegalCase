import React, { useState } from 'react';
import { useMutation } from 'react-query';
import { useForm } from 'react-hook-form';
import styled from 'styled-components';
import toast from 'react-hot-toast';
import { Search, FileText, Clock, CheckCircle, AlertCircle } from 'lucide-react';
import { legalApi } from '../services/api';
import { format } from 'date-fns';

const Container = styled.div`
  max-width: 1400px;
  margin: 0 auto;
  display: grid;
  grid-template-columns: 1fr 2fr;
  gap: 2rem;
  height: calc(100vh - 140px);
`;

const SearchPanel = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 2rem;
  height: fit-content;
`;

const ResultsPanel = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 2rem;
  overflow-y: auto;
`;

const Title = styled.h2`
  color: white;
  margin-bottom: 1.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const Form = styled.form`
  display: flex;
  flex-direction: column;
  gap: 1rem;
`;

const InputGroup = styled.div`
  display: flex;
  flex-direction: column;
  gap: 0.5rem;
`;

const Label = styled.label`
  color: white;
  font-weight: 500;
`;

const TextArea = styled.textarea`
  padding: 1rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: white;
  resize: vertical;
  min-height: 120px;

  &::placeholder {
    color: rgba(255, 255, 255, 0.6);
  }

  &:focus {
    outline: none;
    border-color: rgba(255, 255, 255, 0.5);
  }
`;

const Input = styled.input`
  padding: 0.75rem;
  border: 1px solid rgba(255, 255, 255, 0.3);
  border-radius: 8px;
  background: rgba(255, 255, 255, 0.1);
  color: white;

  &::placeholder {
    color: rgba(255, 255, 255, 0.6);
  }

  &:focus {
    outline: none;
    border-color: rgba(255, 255, 255, 0.5);
  }
`;

const Button = styled.button`
  background: white;
  color: #667eea;
  border: none;
  padding: 1rem 2rem;
  border-radius: 8px;
  font-weight: 600;
  cursor: pointer;
  transition: all 0.2s;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 0.5rem;

  &:hover {
    transform: translateY(-1px);
    box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);
  }

  &:disabled {
    opacity: 0.7;
    cursor: not-allowed;
    transform: none;
  }
`;

const LoadingState = styled.div`
  text-align: center;
  color: white;
  padding: 2rem;
`;

const BriefContainer = styled.div`
  color: white;
`;

const Section = styled.div`
  margin-bottom: 2rem;
  padding-bottom: 1rem;
  border-bottom: 1px solid rgba(255, 255, 255, 0.2);

  &:last-child {
    border-bottom: none;
  }
`;

const SectionTitle = styled.h3`
  color: white;
  margin-bottom: 1rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
`;

const Text = styled.p`
  line-height: 1.6;
  margin-bottom: 1rem;
`;

const List = styled.ul`
  padding-left: 1.5rem;
  line-height: 1.6;
`;

const ListItem = styled.li`
  margin-bottom: 0.5rem;
`;

function Research() {
  const [result, setResult] = useState(null);
  const { register, handleSubmit, reset } = useForm();

  const researchMutation = useMutation(legalApi.research, {
    onSuccess: (data) => {
      setResult(data);
      toast.success('Research completed successfully!');
    },
    onError: (error) => {
      toast.error(error.response?.data?.detail || 'Research failed');
    }
  });

  const onSubmit = (data) => {
    researchMutation.mutate(data);
  };

  return (
    <Container>
      <SearchPanel>
        <Title>
          <Search size={24} />
          Legal Research Query
        </Title>
        <Form onSubmit={handleSubmit(onSubmit)}>
          <InputGroup>
            <Label>Legal Question</Label>
            <TextArea
              {...register('query', { required: true })}
              placeholder="Enter your legal question here... (e.g., 'Can an employer read employee emails?')"
            />
          </InputGroup>
          <InputGroup>
            <Label>Jurisdiction (Optional)</Label>
            <Input
              {...register('jurisdiction')}
              placeholder="e.g., Federal, California, New York"
            />
          </InputGroup>
          <Button type="submit" disabled={researchMutation.isLoading}>
            {researchMutation.isLoading ? (
              <>
                <Clock size={20} />
                Researching...
              </>
            ) : (
              <>
                <Search size={20} />
                Start Research
              </>
            )}
          </Button>
        </Form>
      </SearchPanel>

      <ResultsPanel>
        <Title>
          <FileText size={24} />
          Research Results
        </Title>
        
        {researchMutation.isLoading && (
          <LoadingState>
            <Clock size={48} style={{ marginBottom: '1rem' }} />
            <p>AI agents are working on your research...</p>
            <p style={{ fontSize: '0.9rem', marginTop: '0.5rem', opacity: 0.8 }}>
              This may take 30-60 seconds
            </p>
          </LoadingState>
        )}

        {result && result.success && (
          <BriefContainer>
            <Section>
              <SectionTitle>
                <CheckCircle size={20} />
                Executive Summary
              </SectionTitle>
              <Text>{result.data.brief.executive_summary}</Text>
            </Section>

            <Section>
              <SectionTitle>Key Findings</SectionTitle>
              <List>
                {result.data.brief.key_findings.map((finding, index) => (
                  <ListItem key={index}>{finding}</ListItem>
                ))}
              </List>
            </Section>

            <Section>
              <SectionTitle>Legal Analysis</SectionTitle>
              <Text style={{ whiteSpace: 'pre-line' }}>
                {result.data.brief.legal_analysis}
              </Text>
            </Section>

            <Section>
              <SectionTitle>Conclusions</SectionTitle>
              <List>
                {result.data.brief.conclusions.map((conclusion, index) => (
                  <ListItem key={index}>{conclusion}</ListItem>
                ))}
              </List>
            </Section>

            <Section>
              <SectionTitle>Supporting Cases</SectionTitle>
              <List>
                {result.data.brief.supporting_cases.slice(0, 5).map((citation, index) => (
                  <ListItem key={index}>
                    <strong>{citation.case_name}</strong> - {citation.citation} ({citation.court}, {format(new Date(citation.date), 'yyyy')})
                  </ListItem>
                ))}
              </List>
            </Section>

            <div style={{ fontSize: '0.9rem', opacity: 0.8, marginTop: '2rem' }}>
              Generated on {format(new Date(result.data.brief.generated_at), 'PPpp')}
            </div>
          </BriefContainer>
        )}

        {result && !result.success && (
          <div style={{ color: '#ff6b6b', textAlign: 'center', padding: '2rem' }}>
            <AlertCircle size={48} style={{ marginBottom: '1rem' }} />
            <p>Research failed: {result.error}</p>
          </div>
        )}

        {!result && !researchMutation.isLoading && (
          <div style={{ color: 'rgba(255, 255, 255, 0.6)', textAlign: 'center', padding: '2rem' }}>
            Enter a legal question to begin research
          </div>
        )}
      </ResultsPanel>
    </Container>
  );
}

export default Research; 