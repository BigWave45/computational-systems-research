# Programme: Computational Systems Research

## Purpose

Study the gap between what a computational system is specified or claimed to do, what can actually be observed, and what the available evidence justifies concluding.

A system may include software, agents, APIs, databases, external tools, and the infrastructure connecting them. Behaviour depends on code, state, environment, dependencies, and operating conditions.

## Umbrella question

How can we establish whether a computational system satisfies a stated property under specified operating conditions, given incomplete observation and components outside the evaluator's control?

This is a programme question, not yet a single experiment.

## Working concepts

- **Specification:** a precise statement of expected behaviour or a property.
- **Observation boundary:** events, outputs, state, and interfaces available to an evaluator.
- **Evidence:** recorded observations and artifacts used to support or reject a claim.
- **Verification:** evaluation of whether evidence supports a specified property under stated assumptions.
- **Unknown:** an outcome used when evidence cannot justify either satisfaction or violation.

A useful outcome representation is `SATISFIED | VIOLATED | UNKNOWN`. Three-valued labels do not themselves make a method sound; soundness depends on the property, observation model, oracle, and assumptions.

## Potential domains

AI-agent execution, financial systems, research software, distributed services, and infrastructure are possible application domains. The first study must target one system class and one property.

## Boundaries

The programme does not assume that all behaviour can be inferred from black-box observations; that passing tests prove correctness; that cryptographic integrity proves evidence is truthful or complete; or that controlled experiments establish production guarantees.

## Current state

The initial broad candidate concerned detecting behavioural changes in AI agents. A first prior-art review found substantial existing coverage, including AgentAssay, BehavTest, AgentEval, AEGIS, and recent work on agent tool-action fault injection and authorization. The broad candidate is not being treated as novel.

Independent reproduction and external-validity testing of published assurance results is under consideration. No novelty claim has been made.
