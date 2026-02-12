import { render, screen } from "@testing-library/react";
import { vi } from "vitest";
import StatsPage from "@/app/stats/page";
import { api } from "@/lib/api";

vi.mock("@/lib/api", () => ({
  api: {
    getStats: vi.fn(),
  },
}));

describe("StatsPage", () => {
  it("renders stats after loading", async () => {
    vi.mocked(api.getStats).mockResolvedValueOnce({
      total_laws: 123,
      sources: 2,
    });

    render(<StatsPage />);

    expect(screen.getByTestId("stats-loading")).toBeInTheDocument();

    expect(await screen.findByText("123")).toBeInTheDocument();
    expect(screen.getByText("2")).toBeInTheDocument();
  });

  it("renders error state", async () => {
    vi.mocked(api.getStats).mockRejectedValueOnce(new Error("Boom"));

    render(<StatsPage />);

    expect(await screen.findByText("Boom")).toBeInTheDocument();
  });
});
