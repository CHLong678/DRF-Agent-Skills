# Services, Selectors, and Modules

HackSoftware's Django Styleguide is a useful production reference but intentionally opinionated.

Adapt its ideas conditionally:

- service for meaningful write/workflow orchestration
- selector/query service for complex reusable reads
- model method/property for simple local behavior
- DRF view/serializer for interface concerns

Do not enforce:

- one API class per operation in every project
- APIView over generic views/ViewSets universally
- separate input/output serializer universally
- service/selector wrappers around trivial ORM calls

Preserve local project conventions unless they create concrete correctness, security, performance, or maintainability problems.
