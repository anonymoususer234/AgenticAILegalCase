import React from 'react';
import { Link } from 'react-router-dom';
import styled from 'styled-components';
import { ArrowRight, Brain, Search, FileText, Zap } from 'lucide-react';

const Container = styled.div`
  max-width: 1200px;
  margin: 0 auto;
  text-align: center;
`;

const Hero = styled.section`
  margin-bottom: 4rem;
`;

const Title = styled.h1`
  font-size: 3.5rem;
  font-weight: 800;
  color: white;
  margin-bottom: 1.5rem;
  line-height: 1.2;
`;

const Subtitle = styled.p`
  font-size: 1.25rem;
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 2rem;
  max-width: 600px;
  margin-left: auto;
  margin-right: auto;
`;

const CTAButton = styled(Link)`
  display: inline-flex;
  align-items: center;
  gap: 0.5rem;
  background: white;
  color: #667eea;
  padding: 1rem 2rem;
  border-radius: 12px;
  text-decoration: none;
  font-weight: 600;
  font-size: 1.1rem;
  transition: all 0.3s;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.1);

  &:hover {
    transform: translateY(-2px);
    box-shadow: 0 8px 25px rgba(0, 0, 0, 0.15);
  }
`;

const Features = styled.section`
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
  gap: 2rem;
  margin-bottom: 4rem;
`;

const FeatureCard = styled.div`
  background: rgba(255, 255, 255, 0.1);
  backdrop-filter: blur(10px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  border-radius: 16px;
  padding: 2rem;
  text-align: center;
  transition: transform 0.3s;

  &:hover {
    transform: translateY(-5px);
  }
`;

const FeatureIcon = styled.div`
  color: white;
  margin-bottom: 1rem;
  display: flex;
  justify-content: center;
`;

const FeatureTitle = styled.h3`
  color: white;
  font-size: 1.25rem;
  margin-bottom: 1rem;
`;

const FeatureText = styled.p`
  color: rgba(255, 255, 255, 0.8);
  line-height: 1.6;
`;

function Home() {
  return (
    <Container>
      <Hero>
        <Title>Autonomous Legal Research Assistant</Title>
        <Subtitle>
          Powered by AI agents that retrieve, analyze, and synthesize legal information 
          to generate comprehensive legal briefs with citations.
        </Subtitle>
        <CTAButton to="/research">
          Start Research
          <ArrowRight size={20} />
        </CTAButton>
      </Hero>

      <Features>
        <FeatureCard>
          <FeatureIcon>
            <Search size={48} />
          </FeatureIcon>
          <FeatureTitle>Intelligent Retrieval</FeatureTitle>
          <FeatureText>
            Search across legal databases and case law using advanced AI-powered retrieval agents.
          </FeatureText>
        </FeatureCard>

        <FeatureCard>
          <FeatureIcon>
            <Brain size={48} />
          </FeatureIcon>
          <FeatureTitle>Smart Analysis</FeatureTitle>
          <FeatureText>
            Analyze legal findings for patterns, precedents, and jurisdictional differences.
          </FeatureText>
        </FeatureCard>

        <FeatureCard>
          <FeatureIcon>
            <FileText size={48} />
          </FeatureIcon>
          <FeatureTitle>Structured Briefs</FeatureTitle>
          <FeatureText>
            Generate professional legal briefs with proper citations and jurisdiction analysis.
          </FeatureText>
        </FeatureCard>

        <FeatureCard>
          <FeatureIcon>
            <Zap size={48} />
          </FeatureIcon>
          <FeatureTitle>Autonomous Agents</FeatureTitle>
          <FeatureText>
            Independent AI agents work together with retry logic and self-evaluation.
          </FeatureText>
        </FeatureCard>
      </Features>
    </Container>
  );
}

export default Home; 