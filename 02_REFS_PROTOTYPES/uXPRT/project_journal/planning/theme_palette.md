# Theme Color Palette (Radix UI - Dark Theme)

This document stores the color palette information provided by the user for the XPRT application, intended for use with Radix UI in a dark theme.

## Primary Brand Color (Green)

```css
.dark,
.dark-theme {
  --green-1: #0b1410;
  --green-2: #111c18;
  --green-3: #0d2d23;
  --green-4: #083b2d;
  --green-5: #0f4838;
  --green-6: #1b5644;
  --green-7: #256853;
  --green-8: #2d7e65;
  --green-9: #27b08b;
  --green-10: #0aa47f;
  --green-11: #55d3ac;
  --green-12: #abf0d7;

  --green-a1: #00bc0003;
  --green-a2: #28fab40b;
  --green-a3: #00f8aa1e;
  --green-a4: #00fbb02d;
  --green-a5: #0cfcba3b;
  --green-a6: #36fdc14a;
  --green-a7: #4afec65d;
  --green-a8: #4ffdc975;
  --green-a9: #33ffc8aa;
  --green-a10: #07fec39e;
  --green-a11: #65ffcfd0;
  --green-a12: #b5ffe4ef;

  --green-contrast: #fff;
  --green-surface: #12261f80;
  --green-indicator: #27b08b;
  --green-track: #27b08b;
}

@supports (color: color(display-p3 1 1 1)) {
  @media (color-gamut: p3) {
    .dark,
    .dark-theme {
      --green-1: oklch(18% 0.014 169.6);
      --green-2: oklch(21.4% 0.018 169.6);
      --green-3: oklch(27.2% 0.0423 169.6);
      --green-4: oklch(31.6% 0.0576 169.6);
      --green-5: oklch(36.2% 0.0645 169.6);
      --green-6: oklch(41.1% 0.0685 169.6);
      --green-7: oklch(46.8% 0.0755 169.6);
      --green-8: oklch(53.7% 0.0882 169.6);
      --green-9: oklch(67.8% 0.1256 169.6);
      --green-10: oklch(63.9% 0.1256 169.6);
      --green-11: oklch(78.5% 0.1256 169.6);
      --green-12: oklch(90.3% 0.0778 169.6);

      --green-a1: color(display-p3 0 0.9451 0 / 0.009);
      --green-a2: color(display-p3 0.3373 0.9843 0.7059 / 0.043);
      --green-a3: color(display-p3 0.2784 1 0.7451 / 0.11);
      --green-a4: color(display-p3 0.2745 1 0.7412 / 0.169);
      --green-a5: color(display-p3 0.3608 1 0.7686 / 0.224);
      --green-a6: color(display-p3 0.451 1 0.7882 / 0.283);
      --green-a7: color(display-p3 0.502 0.9961 0.8 / 0.359);
      --green-a8: color(display-p3 0.5176 1 0.8118 / 0.448);
      --green-a9: color(display-p3 0.4784 1 0.8078 / 0.655);
      --green-a10: color(display-p3 0.4392 1 0.7882 / 0.608);
      --green-a11: color(display-p3 0.5765 0.9961 0.8353 / 0.802);
      --green-a12: color(display-p3 0.7804 1 0.9059 / 0.929);

      --green-contrast: #fff;
      --green-surface: color(display-p3 0.0863 0.149 0.1176 / 0.5);
      --green-indicator: oklch(67.8% 0.1256 169.6);
      --green-track: oklch(67.8% 0.1256 169.6);
    }
  }
}
```

## Gray Scale

```css
.dark,
.dark-theme {
  --gray-1: #101211;
  --gray-2: #171918;
  --gray-3: #202322;
  --gray-4: #272a29;
  --gray-5: #2e3130;
  --gray-6: #373b39;
  --gray-7: #444947;
  --gray-8: #5b625f;
  --gray-9: #63706b;
  --gray-10: #717d79;
  --gray-11: #adb5b2;
  --gray-12: #eceeed;

  --gray-a1: #00000000;
  --gray-a2: #f0f2f108;
  --gray-a3: #e7f7f613;
  --gray-a4: #f2fefd1a;
  --gray-a5: #f1fbfa22;
  --gray-a6: #edfbf42d;
  --gray-a7: #edfcf73c;
  --gray-a8: #ebfdf657;
  --gray-a9: #dffdf266;
  --gray-a10: #e5fdf674;
  --gray-a11: #f4fefbb0;
  --gray-a12: #fdfffeed;

  --gray-contrast: #ffffff;
  --gray-surface: rgba(0, 0, 0, 0.05);
  --gray-indicator: #63706b;
  --gray-track: #63706b;
}

@supports (color: color(display-p3 1 1 1)) {
  @media (color-gamut: p3) {
    .dark,
    .dark-theme {
      --gray-1: oklch(18% 0.0036 170.5);
      --gray-2: oklch(21.1% 0.0037 170.5);
      --gray-3: oklch(25.1% 0.004 170.5);
      --gray-4: oklch(28.1% 0.0049 170.5);
      --gray-5: oklch(31.1% 0.0052 170.5);
      --gray-6: oklch(34.7% 0.0061 170.5);
      --gray-7: oklch(39.9% 0.0078 170.5);
      --gray-8: oklch(48.8% 0.0091 170.5);
      --gray-9: oklch(53.3% 0.0175 170.5);
      --gray-10: oklch(57.9% 0.0159 170.5);
      --gray-11: oklch(76.6% 0.01 170.5);
      --gray-12: oklch(94.7% 0.0024 170.5);

      --gray-a1: color(display-p3 0 0 0 / 0);
      --gray-a2: color(display-p3 0.9765 0.9882 0.9843 / 0.03);
      --gray-a3: color(display-p3 0.9922 1 0.9961 / 0.072);
      --gray-a4: color(display-p3 0.9882 0.9961 0.9922 / 0.102);
      --gray-a5: color(display-p3 0.9922 1 0.9961 / 0.131);
      --gray-a6: color(display-p3 0.9725 1 0.9765 / 0.173);
      --gray-a7: color(display-p3 0.9569 1 0.9765 / 0.233);
      --gray-a8: color(display-p3 0.9451 1 0.9725 / 0.338);
      --gray-a9: color(display-p3 0.902 1 0.9569 / 0.397);
      --gray-a10: color(display-p3 0.9216 1 0.9725 / 0.452);
      --gray-a11: color(display-p3 0.9647 1 0.9882 / 0.688);
      --gray-a12: color(display-p3 0.9922 1 0.9961 / 0.929);

      --gray-contrast: #ffffff;
      --gray-surface: color(display-p3 0 0 0 / 5%);
      --gray-indicator: oklch(53.3% 0.0175 170.5);
      --gray-track: oklch(53.3% 0.0175 170.5);
    }
  }
}
```

## Background Color

```css
.dark,
.dark-theme,
:is(.dark, .dark-theme) :where(.radix-themes:not(.light, .light-theme)) {
  --color-background: #101211;
}
```
