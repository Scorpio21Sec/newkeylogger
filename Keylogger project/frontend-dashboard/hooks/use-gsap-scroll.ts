"use client";

import { RefObject, useLayoutEffect } from "react";
import gsap from "gsap";
import { ScrollTrigger } from "gsap/ScrollTrigger";

gsap.registerPlugin(ScrollTrigger);

export function useGsapScroll(ref: RefObject<HTMLElement | null>) {
  useLayoutEffect(() => {
    if (!ref.current) {
      return;
    }

    const context = gsap.context(() => {
      gsap.fromTo(
        "[data-animate='section']",
        { y: 24, opacity: 0, willChange: "transform, opacity" },
        {
          y: 0,
          opacity: 1,
          stagger: 0.12,
          duration: 0.7,
          ease: "power2.out",
          scrollTrigger: {
            trigger: ref.current,
            start: "top 82%",
          },
        },
      );
    }, ref);

    return () => {
      context.revert();
    };
  }, [ref]);
}
