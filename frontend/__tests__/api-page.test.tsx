import { render, screen } from "@testing-library/react";
import ApiPage from "@/app/api/page";

describe("ApiPage", () => {
  it("renders base URL and docs links", () => {
    render(<ApiPage />);

    expect(
      screen.getByRole("heading", { name: /api docs/i })
    ).toBeInTheDocument();

    const baseUrl = screen.getByTestId("api-base-url");
    expect(baseUrl).toHaveTextContent("http://localhost:8000");

    const swagger = screen.getByTestId("swagger-link");
    const redoc = screen.getByTestId("redoc-link");

    expect(swagger).toHaveAttribute("href", "http://localhost:8000/docs");
    expect(redoc).toHaveAttribute("href", "http://localhost:8000/redoc");
  });
});
